# core/views.py

from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Note
from .serializers import UserSerializer, NoteSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .api.responses import error_response
from rest_framework.exceptions import PermissionDenied
# Import our custom throttle
from .throttles import LoginRateThrottle
# Import Celery task
from .tasks import mark_note_as_old

User = get_user_model()

CACHE_TTL = 60 * 5  # cache for 5 minutes


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    permission_classes = [permissions.AllowAny]

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            return {
                "tokens": {"refresh": data["refresh"], "access": data["access"]},
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "role": self.user.role,
                },
            }
        except ValidationError:
            return error_response(
                message="Authentication failed",
                code=status.HTTP_401_UNAUTHORIZED,
                details={"error": "Invalid credentials"},
            )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, IntegrityError):
            return error_response(
                message="User creation failed",
                code=status.HTTP_400_BAD_REQUEST,
                details={"error": "Username already exists"},
            )
        return super().handle_exception(exc)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all() # Default queryset, will be overridden in get_queryset
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(notewriter=self.request.user).order_by("-updated_at")

    @method_decorator(cache_page(CACHE_TTL, cache="default"), name="list")
    @method_decorator(cache_page(CACHE_TTL, cache="default"), name="retrieve")
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(notewriter=self.request.user)
        cache.clear()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.notewriter != self.request.user:
            raise PermissionDenied("You can only edit your own notes")
        serializer.save()
        cache.clear()
        # enqueue Celery task
        mark_note_as_old.delay(instance.id)

    def perform_destroy(self, instance):
        if instance.notewriter != self.request.user:
            raise PermissionDenied("You can only delete your own notes")
        instance.delete()
        cache.clear()

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return error_response(
                message="Permission denied",
                code=status.HTTP_403_FORBIDDEN,
                details={"error": str(exc)},
            )
        return super().handle_exception(exc)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": {"id": user.id, "username": user.username, "role": user.role},
                    "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)},
                },
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return error_response(
                message="Registration failed",
                code=status.HTTP_400_BAD_REQUEST,
                details={"error": "Username already exists"},
            )
        except ValidationError as e:
            return error_response(
                message="Registration failed",
                code=status.HTTP_400_BAD_REQUEST,
                details=e.detail,
            )
        except Exception as e:
            return error_response(
                message="Internal server error",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details={"error": str(e)},
            )
# This view handles user registration, including error handling for common issues.