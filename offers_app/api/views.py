from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min

from offers_app.models import Offer, OfferDetail
from .serializers import OfferCreateSerializer, OfferReadSerializer, OfferReadNoUserDetailsSerializer, OfferDetailReadSerializer, OfferUpdateSerializer
from .permissions import IsBusinessUser, IsOfferOwner
from .paginations import OffersResultPagination
from .filters import OfferFilter

class OffersListView(generics.ListCreateAPIView):
    """
    View for listing and creating offers.
    """
    def get_queryset(self):
        return Offer.objects.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days")
        )
    
    pagination_class = OffersResultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price']

    def get_permissions(self):
        """
        Get permissions based on the request method.
        """
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated() ,IsBusinessUser()]

    def get_serializer_class(self):
        """
        Get the serializer class based on the request method.
        """
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OffersDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting offer details.
    """

    def get_queryset(self):
        """
        Get the queryset with annotated minimum price and delivery time."""
        return Offer.objects.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days")
        )

    def get_permissions(self):
        """
        Get permissions based on the request method.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        """
        Get the serializer class based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return OfferUpdateSerializer
        return OfferReadNoUserDetailsSerializer
    

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting offer details."""
    queryset = OfferDetail.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailReadSerializer
