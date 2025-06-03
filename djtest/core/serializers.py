from rest_framework import serializers
from django.contrib.auth import get_user_model
from.models import *
User=get_user_model
#serializers
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class TakingNote(serializers.ModelSerializer):
    model=Note
    fields=['id','notewriter', 'notes', 'created_at', 'updated_at']
    read_only_fields=['id', 'created_at', 'updated_at']