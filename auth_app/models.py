from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser to include user type.
    """
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    type = models.CharField(max_length=50, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username