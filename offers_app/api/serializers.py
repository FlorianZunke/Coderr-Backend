
from rest_framework import serializers
from django.contrib.auth import get_user_model

from offers_app.models import Offer, OfferDetail


class OfferDetailReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading offer details.
    """
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions",
                  "delivery_time_in_days", "price", "features", "offer_type"]


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username"]


class OfferReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading offers.
    """
    details = OfferDetailReadSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]


class OfferDetailWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing offer details.
    """
    class Meta:
        model = OfferDetail
        fields = ["title", "revisions", "delivery_time_in_days",
                  "price", "features", "offer_type"]


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers.
    """
    details = OfferDetailWriteSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["title", "description", "image", "details"]

    def create(self, validated_data):
        """
        Create a new offer and its details.
        """
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
