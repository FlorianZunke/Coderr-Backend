from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.type})"