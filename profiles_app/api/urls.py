from django.urls import path
from .views import ProfileViewSet


urlpatterns = [
    path('profile/<int:pk>/', ProfileViewSet.as_view(), name='profile-detail'),
    path('profiles/business/', ProfileViewSet.as_view(), name='buisness-profile-list'),
    path('profiles/customer/', ProfileViewSet.as_view(), name='customer-profile-list'),
]