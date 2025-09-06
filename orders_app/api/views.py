from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


from .permissions import IsCustomerUser
from .serializers import OrderListCreateSerializer
from orders_app.models import Order

class OrdersListViewSet(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer
    permission_classes = [IsAuthenticated]


