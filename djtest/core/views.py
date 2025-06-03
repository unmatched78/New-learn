# core/views.py
import logging
from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the base class to get the original tokens
        data = super().validate(attrs)
        # Attach your user info
        data['user'] = {
            'id':       self.user.id,
            'username': self.user.username,
            # add more fields as needed
        }
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # --- Inject these claims into BOTH access & refresh tokens ---
        token['user_id']     = user.id
        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)