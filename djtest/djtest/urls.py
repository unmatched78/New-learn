from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('core.urls') )
]

#serve satatic and media
from django.conf.urls.static import static
from django.conf import settings
from .settings import DEBUG
# handle static files
    
if DEBUG:
    # serve static files and media
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)