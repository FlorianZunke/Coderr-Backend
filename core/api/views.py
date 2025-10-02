from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models

from reviews_app.models import Review
from offers_app.models import Offer
from django.contrib.auth import get_user_model
from .serializers import StatisticsSerializer

class StatisticsView(APIView):
    """
    View to retrieve statistics about the platform.
    """
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        Retrieve statistics including review count, average rating,
        business profile count, and offer count.
        """
        review_count = Review.objects.count()
        average_rating = (
            round(Review.objects.all().aggregate(avg=models.Avg("rating"))["avg"] or 0, 1)
        )
        User = get_user_model()
        business_profile_count = User.objects.filter(type="business").count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)