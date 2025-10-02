from rest_framework import serializers
from profiles_app.models import Profile
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    type = serializers.CharField(source='user.type', read_only=True)
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)

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

    def update(self, instance, validated_data):
        """
        Update the user profile.
        """
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for business profiles.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
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
    """
    Serializer for customer profiles.
    """
    username = serializers.CharField(source='user.username',read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
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
