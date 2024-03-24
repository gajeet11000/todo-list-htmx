from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class List(models.Model):
    title = models.CharField(max_length=24, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
class Task(models.Model):
    task = models.CharField(max_length=64)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    
    date = models.DateTimeField(auto_now_add=True)