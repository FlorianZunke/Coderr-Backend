from django.urls import path
from .views import OffersListView, OffersDetailView, OfferDetailView


urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', OffersDetailView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetail-detail'),
]