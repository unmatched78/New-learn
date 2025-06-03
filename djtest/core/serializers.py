from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Note
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
User = get_user_model()  
# serializers.py

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password',  'role']
    
    def validate_password(self, value):
        try:
            # Enforce Django's password validators
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Passwords must match"})
    #     return attrs
    
    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hashes the password
        user.save()
        return user
class NoteSerializer(serializers.ModelSerializer):  
    notewriter = UserSerializer(read_only=True)  
    
    class Meta:
        model = Note
        fields = ['id', 'notewriter', 'content', 'created_at', 'updated_at']  
        read_only_fields = ['id', 'created_at', 'updated_at', 'notewriter']  