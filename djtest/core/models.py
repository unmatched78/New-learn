from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime
# Create your models here.
class Timer(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class meta:
        abstract=True

class CustomUser(AbstractUser):
    Roles=[
        ("boy","BOY"),
        ("girl","GIRL"),
    ]
    role=models.CharField(choices=Roles, default="boy")
    def __str__(self):
        return f"{self.username} --{self.role}."

class Note(Timer):
    notewriter=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="notewriter")
    notes=models.TextField()
    def __str__(self):
        return f"{self.note[:20]} by {self.notewriter.username if self.notewriter else 'Anonymous'}"

    
