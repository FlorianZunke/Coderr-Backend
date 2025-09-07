from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView

from offers_app.models import OfferDetail
from orders_app.models import Order

from .permissions import IsCustomerUser
from .serializers import OrderListCreateSerializer, OrderCreateFromOfferDetailSerializer


class OrdersListViewSet(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomerUser()]

    def get(self, request):
        orders_customer = Order.objects.filter(customer_user=request.user)
        orders_business = Order.objects.filter(business_user=request.user)
        orders = orders_customer | orders_business
        orders = orders.distinct()
        serializer = OrderListCreateSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_detail_id = serializer.validated_data.get("offer_detail_id")
        if not offer_detail_id:
            return Response(
                {"detail": "'offer_detail_id' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            offer_detail = OfferDetail.objects.select_related(
                "offer").get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response(
                {"detail": "OfferDetail not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

        output_serializer = OrderListCreateSerializer(
            order, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
