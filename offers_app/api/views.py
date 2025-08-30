from rest_framework import generics
from rest_framework.permissions import IsAuthenticated



from offers_app.models import Offer
from .serializers import OfferSerializer
from .permissions import IsBusinessUser


class OffersListView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]