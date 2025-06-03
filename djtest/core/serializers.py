from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()  
# serializers.py
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'boy')
        )
        return user

class NoteSerializer(serializers.ModelSerializer):  
    notewriter = UserSerializer(read_only=True)  
    
    class Meta:
        model = Note
        fields = ['id', 'notewriter', 'content', 'created_at', 'updated_at']  
        read_only_fields = ['id', 'created_at', 'updated_at', 'notewriter']  