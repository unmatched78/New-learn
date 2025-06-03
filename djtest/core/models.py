from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Timer(models.Model):
    created_at=models.DateTimeField(auto_add_now=True)
    updated_at=models.DateTimeField(auto_now=True)
    class meta:
        abstract=True

class CustomUser(AbstractUser):
    Roles=[
        ("boy":"BOY"),
        ("girl":"GIRL"),
    ]
    role=models.CharField(choices=Roles, default="boy")
    def __str__(self):
        return f"{self.username} --{self.role}."

class Note(Timer):
    notewriter=models.Foreignkey(CustomUser, on_delete=models.set_null, related_name="notewriter")
    note=models.TextField()
    def __str__(self):
        return f"{self.note[:20]} by {self.notewriter.username}"


    
