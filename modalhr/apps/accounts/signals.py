# apps/accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, TenantUser
from apps.tenants.models import Tenant

@receiver(post_save, sender=User)
def create_tenant_user(sender, instance, created, **kwargs):
    """Create TenantUser for new User if they belong to a tenant."""
    if created:
        # Example: If user is created with a tenant context (e.g., via API), link them
        from apps.core.utils import get_current_tenant
        tenant = get_current_tenant()
        if tenant:
            TenantUser.objects.create(
                user=instance,
                tenant=tenant,
                role='employee',  # Default role
                status='active'
            )