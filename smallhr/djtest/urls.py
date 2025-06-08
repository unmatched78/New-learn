from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('core.urls') ),
    path('', TemplateView.as_view(template_name='index.html'), name='app'),
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