from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from offers_app.models import Offer
from .serializers import OfferCreateSerializer, OfferReadSerializer
from .permissions import IsBusinessUser


class OffersListView(generics.ListCreateAPIView):
    """
    View for listing and creating offers.
    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser]

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
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def get_serializer_class(self):
        """
        Get the serializer class based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return OfferCreateSerializer
        return OfferReadSerializer
