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


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetail-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading offers.
    """
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    min_delivery_time = serializers.IntegerField(
        read_only=True
    )
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


class OfferReadNoUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for reading offers without user_details.
    """
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    min_delivery_time = serializers.IntegerField(
        read_only=True
    )

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

    def update(self, instance, validated_data):
        """
        Update offer and its details.
        """
        details_data = validated_data.pop("details", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            """
            Mapping: (id, offer_type) -> OfferDetail
            """
            existing_details = {(detail.id, detail.offer_type): detail for detail in instance.details.all()}
            sent_ids_types = set()
            for detail_data in details_data:
                detail_id = detail_data.get("id")
                offer_type = detail_data.get("offer_type")
                sent_ids_types.add((detail_id, offer_type))
                if detail_id and (detail_id, offer_type) in existing_details:
                    detail_instance = existing_details[(detail_id, offer_type)]
                    for attr, value in detail_data.items():
                        if attr != "id":
                            setattr(detail_instance, attr, value)
                    detail_instance.save()
                else:
                    OfferDetail.objects.create(offer=instance, **detail_data)
        return instance
