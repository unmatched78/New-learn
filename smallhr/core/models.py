from django.db import models
from django.contrib.auth.models import AbstractUser

class Timer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class CustomUser(AbstractUser):
    ROLES = [
        ("boy", "BOY"),
        ("girl", "GIRL"),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default="boy")
    
    def __str__(self):
        return f"{self.username} -- {self.role}"

class Note(Timer):
    notewriter = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name="notes"
    )
    content = models.TextField()  
    
    def __str__(self):
        
        return f"{self.content[:20]} by {self.notewriter.username if self.notewriter else 'Anonymous'}"