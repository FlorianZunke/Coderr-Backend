from rest_framework import serializers


from reviews_app.models import Review





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "reviewer", "business_user", "rating", "description", "created_at"]
        read_only_fields = ["id", "reviewer", "created_at"]