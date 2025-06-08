# apps/core/middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
import pytz

from apps.core.managers import set_current_tenant, set_current_user
from apps.core.models import AuditLog

logger = logging.getLogger(__name__)

class TimezoneMiddleware(MiddlewareMixin):
    """Middleware to set timezone based on authenticated user's preference."""

    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            user_tz = getattr(user, 'timezone', None)
            if user_tz:
                try:
                    timezone.activate(pytz.timezone(user_tz))
                except Exception:
                    logger.warning(f"Invalid timezone {user_tz}, deactivating.")
                    timezone.deactivate()
                return
        # Default fallback
        timezone.deactivate()

class AuditMiddleware(MiddlewareMixin):
    """Middleware to set thread-local context and log audit entries for API calls."""

    def process_request(self, request):
        # Set user context
        user = getattr(request, 'user', None)
        if user and not isinstance(user, AnonymousUser):
            set_current_user(user)

        # Set tenant context
        tenant = getattr(request, 'tenant', None)
        if tenant:
            set_current_tenant(tenant)

    def process_response(self, request, response):
        try:
            user = getattr(request, 'user', None)
            tenant = getattr(request, 'tenant', None)

            is_api = request.path.startswith('/api/')
            valid_user = user and not isinstance(user, AnonymousUser)
            if is_api and valid_user and tenant and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                AuditLog.objects.create(
                    tenant=tenant,
                    user=user,
                    action='API_CALL',
                    description=f"{request.method} {request.get_full_path()}",
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    changes={'status_code': response.status_code}
                )
        except Exception:
            logger.error("Failed to create audit log", exc_info=True)

        return response

    def get_client_ip(self, request):
        """Retrieve the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For may contain multiple IPs, take the first
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
