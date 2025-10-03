from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

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
        fields = ["id","title", "revisions", "delivery_time_in_days",
                  "price", "features", "offer_type"]
        
    def to_internal_value(self, data):
        allowed = set(self.fields.keys())
        extra = set(data.keys()) - allowed
        if extra:
            raise serializers.ValidationError(f"Unerwartete Felder: {', '.join(extra)}")
        return super().to_internal_value(data)


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers.
    """
    details = OfferDetailWriteSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "description", "image", "details"]

    def create(self, validated_data):
        """
        Create a new offer and its details.
        """
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offers and their details.
    """
    details = OfferDetailWriteSerializer(many=True, required=True)
    title = serializers.CharField(write_only=True, required=False)
    description = serializers.CharField(write_only=True, required=False)
    image = serializers.ImageField(write_only=True, required=False)


    class Meta:
        model = Offer
        fields = ["id", "title", "description", "image", "details"]

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data.get("offer_type")
            if not offer_type:
                raise serializers.ValidationError(
                    {"details": "Jedes Detail muss ein 'offer_type' enthalten."}
                )

            try:
                detail = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"OfferDetail mit offer_type '{offer_type}' existiert nicht."}
                )

            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()

        return instance