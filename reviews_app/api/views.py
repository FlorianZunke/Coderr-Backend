from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from reviews_app.models import Review
from .serializers import ReviewCreateSerializer
from .permissions import IsReviewOwner, IsCustomerUser

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]

    def perform_create(self, serializer):
        reviewer = self.request.user
        business_user_id = serializer.validated_data["business_user"]

        User = get_user_model()
        try:
            business_user_obj = User.objects.get(pk=business_user_id.id if hasattr(business_user_id, "id") else business_user_id)
        except User.DoesNotExist:
            raise ValidationError("Das angegebene Geschäftsprofil existiert nicht.")

        if getattr(business_user_obj, "type", None) != "business":
            raise ValidationError("Das angegebene Profil ist kein Geschäftsprofil.")

        # Prüfe, ob bereits eine Bewertung existiert
        if Review.objects.filter(reviewer=reviewer, business_user=business_user_obj).exists():
            raise ValidationError("Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben.")

        serializer.save(reviewer=reviewer, business_user=business_user_obj)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]