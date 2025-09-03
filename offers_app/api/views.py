from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend



from offers_app.models import Offer
from .serializers import OfferCreateSerializer, OfferReadSerializer
from .permissions import IsBusinessUser
from .paginations import OffersResultPagination
from .filters import OfferFilter



class OffersListView(generics.ListCreateAPIView):
    """
    View for listing and creating offers.
    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser]
    pagination_class = OffersResultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price'] #min_price funktioniert noch nciht beim ordering

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
    #Bei den Details muss noch eine URl anstelle von den ganzen Details eingefügt werden
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
