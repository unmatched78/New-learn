from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()  
# serializers.py
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'role']
    
    def validate_password(self, value):
        try:
            # Enforce Django's password validators
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs
    
    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hashes the password
        user.save()
        return user

class AuthResponseSerializer(serializers.Serializer):
    tokens = serializers.DictField(child=serializers.CharField())
    user = UserSerializer()

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Note
from bleach import clean

User = get_user_model()

class NoteSerializer(serializers.ModelSerializer):
    notewriter = serializers.SerializerMethodField()
    
    class Meta:
        model = Note
        fields = ['id', 'notewriter', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'notewriter']

    def get_notewriter(self, obj):
        if obj.notewriter:
            return {'id': obj.notewriter.id, 'username': obj.notewriter.username, 'role': obj.notewriter.role}
        return None

    def validate_content(self, value):
        # Sanitize HTML content
        return clean(value, tags=['p', 'b', 'i', 'u', 'strong', 'em', 'ul', 'li', 'ol'], attributes={})