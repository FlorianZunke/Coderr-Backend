
from rest_framework import serializers
from profiles_app.models import Profile
from auth_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "type"]

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

class BusinessSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)  
    type = serializers.CharField(source='user.type', read_only=True)
    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type",
        ]
