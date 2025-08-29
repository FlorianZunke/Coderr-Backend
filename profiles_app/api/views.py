from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from auth_app.models import CustomUser
from profiles_app.models import Profile
from profiles_app.api.serializers import ProfileSerializer, BusinessSerializer, CustomerSerializer
from .permissions import SelfUserOrReadOnly



class ProfileViewSet(generics.RetrieveUpdateAPIView):
    """
    View for user profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, SelfUserOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get("pk")
        user = get_object_or_404(CustomUser, pk=user_id)
        return get_object_or_404(Profile, user=user)
    

class BusinessProfileListView(generics.ListAPIView):
    """
    View for business profile list.
    """
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        queryset = queryset.filter(user__type ="business")

        return queryset

class CustomerProfileListView(generics.ListAPIView):
    """
    View for customer profile list.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        queryset = queryset.filter(user__type ="customer")

        return queryset 
    