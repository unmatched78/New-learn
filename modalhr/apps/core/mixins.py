# apps/core/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class TenantRequiredMixin:
    """Mixin to ensure tenant is set for the request"""
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'tenant') or not request.tenant:
            raise PermissionDenied("Tenant is required for this request")
        return super().dispatch(request, *args, **kwargs)

class ModuleRequiredMixin:
    """Mixin to check if required module is active for tenant"""
    required_module = None
    
    def dispatch(self, request, *args, **kwargs):
        if self.required_module:
            from apps.module_manager.utils import is_module_active
            if not is_module_active(request.tenant, self.required_module):
                raise PermissionDenied(f"Module '{self.required_module}' is not active")
        return super().dispatch(request, *args, **kwargs)

class AuditMixin:
    """Mixin to automatically create audit logs"""
    
    def perform_create(self, serializer):
        instance = serializer.save()
        self.create_audit_log('CREATE', instance)
        return instance
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        instance = serializer.save()
        self.create_audit_log('UPDATE', instance, old_instance)
        return instance
    
    def perform_destroy(self, instance):
        self.create_audit_log('DELETE', instance)
        instance.delete()
    
    def create_audit_log(self, action, instance, old_instance=None):
        from apps.core.models import AuditLog
        from apps.core.utils import get_model_changes
        
        changes = {}
        if old_instance and action == 'UPDATE':
            changes = get_model_changes(old_instance, instance)
        
        AuditLog.objects.create(
            tenant=self.request.tenant,
            user=self.request.user,
            action=action,
            content_object=instance,
            changes=changes,
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            module=getattr(self, 'module_name', ''),
            description=f"{action} {instance._meta.verbose_name}"
        )
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class StandardResponseMixin:
    """Mixin to standardize API responses"""
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)