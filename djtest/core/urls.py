from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    MyTokenObtainPairView,
    UserViewSet,
    NoteViewSet,
    RegisterView
)

from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),#for api users
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]