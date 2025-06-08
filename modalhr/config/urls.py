# config/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

# Core/public routes (public schema)
urlpatterns = [
    path(f'api/{settings.API_VERSION}/auth/',    include('apps.accounts.urls')),
    path(f'api/{settings.API_VERSION}/tenants/', include('apps.tenants.urls')),
    path(f'api/{settings.API_VERSION}/modules/', include('apps.module_manager.urls')),
]

# Dynamically include each HR module based on your ENABLED_MODULES setting
ENABLED = config(
    'ENABLED_MODULES',
    default='employees,time_attendance,leave_management,payroll,performance,recruitment,benefits,learning'
).split(',')

for mod in ENABLED:
    urlpatterns.append(
        path(
            f'api/{settings.API_VERSION}/{mod.replace("_", "-")}/',
            include(f'apps.hr_modules.{mod}.urls')
        )
    )

# Serve static & media files in DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
