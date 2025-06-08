# apps/core/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from apps.core.managers import get_current_tenant
from apps.module_manager.utils import is_module_active, has_module_permission
from apps.core.models import AuditLog
from apps.core.utils import get_model_changes

class TenantRequiredMixin(AccessMixin):
    """Ensure the request has a tenant set."""
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'tenant') or not request.tenant:
            raise PermissionDenied("Tenant is required for this request")
        return super().dispatch(request, *args, **kwargs)

class ModuleRequiredMixin(AccessMixin):
    """Ensure a required module is active for the tenant."""
    required_module = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_module:
            tenant = getattr(request, 'tenant', None)
            if not tenant or not is_module_active(tenant, self.required_module):
                raise PermissionDenied(f"Module '{self.required_module}' is not active")
        return super().dispatch(request, *args, **kwargs)

class AuditMixin:
    """Mixin to create audit logs on create, update, and delete."""
    module_name = None  # set in subclass to annotate logs

    def perform_create(self, serializer):
        instance = serializer.save()
        self._create_audit('CREATE', instance)
        return instance

    def perform_update(self, serializer):
        old = self.get_object()
        instance = serializer.save()
        self._create_audit('UPDATE', instance, old)
        return instance

    def perform_destroy(self, instance):
        self._create_audit('DELETE', instance)
        instance.delete()

    def _create_audit(self, action, instance, old_instance=None):
        request = getattr(self, 'request', None)
        if not request:
            return
        try:
            changes = {}
            if old_instance and action == 'UPDATE':
                changes = get_model_changes(old_instance, instance)

            AuditLog.objects.create(
                tenant=request.tenant,
                user=request.user,
                action=action,
                content_object=instance,
                changes=changes,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                module=self.module_name or '',
                description=f"{action} {instance._meta.verbose_name}"
            )
        except Exception:
            pass  # avoid blocking main flow

    def _get_client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

class StandardResponseMixin:
    """Mixin to standardize DRF viewset responses."""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'success': True, 'message': 'Created successfully', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated = self.perform_update(serializer)
        return Response(
            {'success': True, 'message': 'Updated successfully', 'data': serializer.data}
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'success': True, 'message': 'Deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
