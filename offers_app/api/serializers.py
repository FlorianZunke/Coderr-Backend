
from rest_framework import serializers

from offers_app.models import Offer



class OfferReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id','user','title','image','description','created_at','updated_at','details' ,'min_price', 'min_delivery_time', 'user_details']




class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'image', 'min_price', 'min_delivery_time']