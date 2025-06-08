# apps/core/permissions.py
from rest_framework import permissions
from apps.module_manager.utils import is_module_active, has_module_permission

class TenantPermission(permissions.BasePermission):
    """Permission to check if user belongs to the tenant"""
    
    def has_permission(self, request, view):
        if not hasattr(request, 'tenant') or not request.tenant:
            return False
        
        if not request.user.is_authenticated:
            return False
        
        # Check if user belongs to the tenant
        return request.user.tenants.filter(id=request.tenant.id).exists()

class ModulePermission(permissions.BasePermission):
    """Permission to check if module is active and user has permission"""
    
    def has_permission(self, request, view):
        module_name = getattr(view, 'module_name', None)
        if not module_name:
            return True
        
        # Check if module is active for tenant
        if not is_module_active(request.tenant, module_name):
            return False
        
        # Check if user has permission for the module
        permission = getattr(view, 'module_permission', 'view')
        return has_module_permission(request.user, module_name, permission)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to allow owners to edit their own objects"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.created_by == request.user