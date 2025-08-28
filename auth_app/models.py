from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    type = models.CharField(max_length=50, choices=USER_TYPES)

    def __str__(self):
        return self.username