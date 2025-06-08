# apps/core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from apps.core.managers import set_current_tenant, set_current_user
from apps.core.models import AuditLog
import pytz

class TimezoneMiddleware(MiddlewareMixin):
    """Middleware to set timezone based on user preference"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            user_timezone = getattr(request.user, 'timezone', None)
            if user_timezone:
                timezone.activate(pytz.timezone(user_timezone))
            else:
                timezone.deactivate()

class AuditMiddleware(MiddlewareMixin):
    """Middleware to create audit logs for requests"""
    
    def process_request(self, request):
        # Set current user in thread local
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            set_current_user(request.user)
        
        # Set current tenant in thread local
        if hasattr(request, 'tenant'):
            set_current_tenant(request.tenant)
    
    def process_response(self, request, response):
        # Log API requests
        if (request.path.startswith('/api/') and 
            hasattr(request, 'user') and 
            not isinstance(request.user, AnonymousUser) and
            hasattr(request, 'tenant')):
            
            # Only log certain methods
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                try:
                    AuditLog.objects.create(
                        tenant=request.tenant,
                        user=request.user,
                        action='API_CALL',
                        description=f"{request.method} {request.path}",
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        changes={'status_code': response.status_code}
                    )
                except Exception:
                    pass  # Don't break request if audit log fails
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip