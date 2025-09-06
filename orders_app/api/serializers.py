# filepath: d:\Weiterbildung\Projekte_Backend\Coderr-Backend\orders_app\api\serializers.py
from rest_framework import serializers

# Importiere dein Order-Modell
from orders_app.models import Order

class OrderListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
