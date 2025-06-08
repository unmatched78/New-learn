# apps/core/permissions.py
from rest_framework import permissions
from apps.module_manager.utils import is_module_active, has_module_permission
from django.core.exceptions import PermissionDenied

class TenantPermission(permissions.BasePermission):
    """Ensure the user is authenticated and belongs to the current tenant."""

    def has_permission(self, request, view):
        tenant = getattr(request, 'tenant', None)
        user = request.user

        if not tenant:
            return False
        if not user or not user.is_authenticated:
            return False

        # If user model has a 'tenants' relationship
        if hasattr(user, 'tenants'):
            return user.tenants.filter(id=tenant.id).exists()

        # Fallback: assume user has direct tenant attribute
        if hasattr(user, 'current_tenant'):
            return user.current_tenant.id == tenant.id

        return False

class ModulePermission(permissions.BasePermission):
    """Ensure the module is active for the tenant and user has the required permission."""

    def has_permission(self, request, view):
        tenant = getattr(request, 'tenant', None)
        user = request.user
        module_name = getattr(view, 'module_name', None)
        required_perm = getattr(view, 'module_permission', 'view')

        if not module_name or not tenant:
            return True  # No module constraint

        if not is_module_active(tenant, module_name):
            return False

        return has_module_permission(user, module_name, required_perm)

class OwnerOrReadOnly(permissions.BasePermission):
    """Allow read-only access to all, write access only to the owner of an object."""

    def has_object_permission(self, request, view, obj):
        # Safe methods are allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Ensure obj has 'created_by' attribute
        owner = getattr(obj, 'created_by', None)
        return owner and owner == request.user

class AdminOrReadOnly(permissions.BasePermission):
    """Allow write access only to users with is_staff or is_superuser."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

class AlwaysAllow(permissions.BasePermission):
    """A permission class that always grants access."""
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return True
