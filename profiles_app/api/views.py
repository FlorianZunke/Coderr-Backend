from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from auth_app.models import CustomUser
from profiles_app.models import Profile
from profiles_app.api.serializers import ProfileSerializer



class ProfileViewSet(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get("pk")
        user = get_object_or_404(CustomUser, pk=user_id)
        return get_object_or_404(Profile, user=user)