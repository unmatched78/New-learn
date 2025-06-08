# apps/core/managers.py
from django.db import models
from django.utils import timezone
from threading import local

_thread_locals = local()

def get_current_tenant():
    """Get current tenant from thread local storage"""
    return getattr(_thread_locals, 'tenant', None)


def set_current_tenant(tenant):
    """Set current tenant in thread local storage"""
    _thread_locals.tenant = tenant


def get_current_user():
    """Get current user from thread local storage"""
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """Set current user in thread local storage"""
    _thread_locals.user = user


class TenantAwareManager(models.Manager):
    """Manager that automatically filters by current tenant"""

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = get_current_tenant()
        if tenant is not None:
            return queryset.filter(tenant=tenant)
        return queryset

    def all_tenants(self):
        """Get objects from all tenants (admin use)"""
        return super().get_queryset()


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted objects by default"""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self):
        """Include soft-deleted objects"""
        return super().get_queryset()

    def deleted_only(self):
        """Get only soft-deleted objects"""
        return super().get_queryset().filter(is_deleted=True)


class BaseManager(TenantAwareManager, SoftDeleteManager):
    """Combined manager for base model functionality"""
    def get_queryset(self):
        # Start with base queryset excluding deleted
        qs = super(SoftDeleteManager, self).get_queryset()
        tenant = get_current_tenant()
        if tenant is not None:
            qs = qs.filter(tenant=tenant)
        return qs.filter(is_deleted=False)
