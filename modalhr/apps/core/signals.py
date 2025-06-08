# apps/core/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from apps.core.models import AuditLog
from apps.core.managers import get_current_tenant, get_current_user

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login"""
    if hasattr(request, 'tenant'):
        AuditLog.objects.create(
            tenant=request.tenant,
            user=user,
            action='LOGIN',
            description='User logged in',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout"""
    if hasattr(request, 'tenant') and user:
        AuditLog.objects.create(
            tenant=request.tenant,
            user=user,
            action='LOGOUT',
            description='User logged out',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip