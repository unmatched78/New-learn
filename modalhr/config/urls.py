### config/urls.py

from django.urls import path, include
from django.conf import settings

# Core/public routes (public schema)
urlpatterns = [
    path(f'api/{settings.API_VERSION}/auth/', include('apps.accounts.urls')),
    path(f'api/{settings.API_VERSION}/tenants/', include('apps.tenants.urls')),
    path(f'api/{settings.API_VERSION}/modules/', include('apps.module_manager.urls')),
]

# Tenant-scoped module URLs
for mod in config(
    'ENABLED_MODULES',
    default='employees,time_attendance,leave_management,payroll,performance,recruitment,benefits,learning'
).split(','):
    urlpatterns.append(
        path(
            f'api/{settings.API_VERSION}/{mod.replace("_", "-")}/',
            include(f'apps.hr_modules.{mod}.urls')
        )
    )

# Static & media in DEBUG\ nfrom django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
