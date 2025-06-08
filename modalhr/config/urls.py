from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path(f'api/{settings.API_VERSION}/auth/', include('apps.accounts.urls')),
    path(f'api/{settings.API_VERSION}/tenants/', include('apps.tenants.urls')),
    path(f'api/{settings.API_VERSION}/modules/', include('apps.module_manager.urls')),
    
    # HR Modules
    path(f'api/{settings.API_VERSION}/employees/', include('apps.hr_modules.employees.urls')),
    path(f'api/{settings.API_VERSION}/time-attendance/', include('apps.hr_modules.time_attendance.urls')),
    path(f'api/{settings.API_VERSION}/payroll/', include('apps.hr_modules.payroll.urls')),
    # Add other modules similarly
]

# Conditionally enable modules
if settings.MODULES_ENABLED.get('leave_management', False):
    urlpatterns.append(path(f'api/{settings.API_VERSION}/leave/', include('apps.hr_modules.leave_management.urls')))
#serve satatic and media
from django.conf.urls.static import static
from django.conf import settings
from .settings import DEBUG
# handle static files
    
if DEBUG:
    # serve static files and media
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)