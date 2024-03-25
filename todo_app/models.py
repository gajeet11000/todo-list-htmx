from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class List(models.Model):
    title = models.CharField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "user"], name="composite_pk")
        ]
    
class Task(models.Model):
    name = models.CharField(max_length=64)
    completed = models.BooleanField(default=False)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    
    date = models.DateTimeField(auto_now_add=True)