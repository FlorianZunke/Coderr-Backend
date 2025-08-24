
from rest_framework import serializers
from profiles_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type', 
            'email', 
            'created_at'
            ]