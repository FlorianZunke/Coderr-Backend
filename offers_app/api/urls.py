from django.urls import path
from .views import OffersListView, OffersDetailView


urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers-list'),
    path('offers/<int:id>/', OffersDetailView.as_view(), name='offers-detail'),
    path('offerdetails/<int:id>/', OffersDetailView.as_view(), name='offersdetail-detail'),
]