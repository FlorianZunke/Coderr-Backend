from rest_framework import serializers

from reviews_app.models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and reading reviews.
    """
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, updating, and deleting reviews.
    """
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        """
        Only 'rating' and 'description' fields can be updated.
        """
        allowed = {"rating", "description"}
        if set(attrs.keys()) - allowed:
            raise serializers.ValidationError("Nur die Felder 'rating' und 'description' dürfen geändert werden.")
        return attrs