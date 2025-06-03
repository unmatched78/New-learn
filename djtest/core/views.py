# core/views.py
from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .api.responses import error_response  # Import the helper
from rest_framework.exceptions import PermissionDenied
User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    permission_classes = [permissions.AllowAny]
    def validate(self, attrs):
        try:
            # Call the base class to get the original tokens
            data = super().validate(attrs)
            
            # Return the same structure as registration
            return {
                "tokens": {
                    "refresh": data["refresh"],
                    "access": data["access"]
                },
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "role": self.user.role
                }
            }
        except ValidationError as e:
            # Handle authentication failures
            return error_response(
                message="Authentication failed",
                code=status.HTTP_401_UNAUTHORIZED,
                details={"error": "Invalid credentials"}
            )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def handle_exception(self, exc):
        # Custom exception handling for UserViewSet
        if isinstance(exc, IntegrityError):
            return error_response(
                message="User creation failed",
                code=status.HTTP_400_BAD_REQUEST,
                details={"error": "Username already exists"}
            )
        return super().handle_exception(exc)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()

    def get_queryset(self):
        # Return only the current user's notes
        return Note.objects.filter(notewriter=self.request.user)

    def perform_create(self, serializer):
        # Automatically set notewriter to current user
        serializer.save(notewriter=self.request.user)

    def perform_update(self, serializer):
        # Ensure user can only update their own notes
        if self.get_object().notewriter != self.request.user:
            raise PermissionDenied("You can only edit your own notes")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure user can only delete their own notes
        if instance.notewriter != self.request.user:
            raise PermissionDenied("You can only delete your own notes")
        instance.delete()

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return error_response(
                message="Permission denied",
                code=status.HTTP_403_FORBIDDEN,
                details={"error": str(exc)}
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
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            
        except IntegrityError as e:
            # Handle duplicate username
            return error_response(
                message="Registration failed",
                code=status.HTTP_400_BAD_REQUEST,
                details={"error": "Username already exists"}
            )
            
        except ValidationError as e:
            # Handle password validation errors
            return error_response(
                message="Registration failed",
                code=status.HTTP_400_BAD_REQUEST,
                details=e.detail
            )
            
        except Exception as e:
            # Handle unexpected errors
            return error_response(
                message="Internal server error",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details={"error": str(e)}
            )