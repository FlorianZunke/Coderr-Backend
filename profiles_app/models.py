from django.db import models
from auth_app.models import CustomUser

    

class Profile(models.Model):
    """
    Model representing a user profile with additional information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"