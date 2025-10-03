from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404

from offers_app.models import OfferDetail
from orders_app.models import Order
from auth_app.models import CustomUser

from .permissions import IsCustomerUser, IsBusinessUser, IsStaffUser
from .serializers import OrderListCreateSerializer, OrderDetailSerializer


class OrdersListViewSet(ListCreateAPIView):
    """
    View for listing and creating orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomerUser()]

    def get(self, request):
        """
        List orders for the authenticated user, either as a customer or business user.
        """
        orders_customer = Order.objects.filter(customer_user=request.user)
        orders_business = Order.objects.filter(business_user=request.user)
        orders = orders_customer | orders_business
        orders = orders.distinct()
        serializer = OrderListCreateSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new order based on the provided offer_detail_id.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_detail_id = serializer.validated_data.get("offer_detail_id")
        if not offer_detail_id:
            return Response(
                {"detail": "'offer_detail_id' is required and must be provided in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            offer_detail = OfferDetail.objects.select_related(
                "offer").get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response(
                {"detail": f"OfferDetail with id {offer_detail_id} not found."},
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


class OrderDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUser()]
        if self.request.method == 'DELETE':
            return [IsStaffUser()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """
        Update only the 'status' field of the order.
        """
        allowed_fields = {"status"}
        if set(request.data.keys()) - allowed_fields:
            return Response(
                {"detail": "Ungültiger Status oder unzulässige Felder in der Anfrage."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


class OrderBusinessCountView(APIView):
    """
    View to return the count of open orders for a given business user ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        business_user = get_object_or_404(CustomUser, pk=pk, type="business")

        count = Order.objects.filter(
            business_user=business_user,
            status="in_progress"
        ).count()

        return Response({"order_count": count})
    

class OrderCompletedCountView(APIView):
    """
    View to return the count of completed orders for a given business user ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        business_user = get_object_or_404(CustomUser, pk=pk, type="business")

        count = Order.objects.filter(
            business_user=business_user,
            status="completed"
        ).count()

        return Response({"completed_order_count": count})
