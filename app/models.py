
from django.db import models
# Create your models here.

from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    