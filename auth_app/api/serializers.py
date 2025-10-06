from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from auth_app.models import CustomUser
from profiles_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.
    """
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'type': {
                'write_only': True
            }
        }

    def save(self, **kwargs):

        """
        Save the user account.
        """
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})

        account = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            type=self.validated_data['type'],
        )
        account.set_password(pw)
        account.save()
        Profile.objects.create(user=account) 
        return account
    

class CustomLoginSerializer(serializers.Serializer):

    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate user credentials.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError({'error': 'Invalid credentials'})
        data['user'] = user
        return data

    def create(self, validated_data):
        return validated_data