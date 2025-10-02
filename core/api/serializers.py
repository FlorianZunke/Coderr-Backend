from rest_framework import serializers

class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for platform statistics.
    """
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()