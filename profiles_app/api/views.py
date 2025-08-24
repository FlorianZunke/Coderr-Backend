from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from permissions import IsAuthenticated

from profiles_app.models import Profile
from profiles_app.api.serializers import ProfileSerializer



class ProfileViewSet(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]