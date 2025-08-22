from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    type = models.CharField(max_length=50, default='customer')

    def __str__(self):
        return self.username