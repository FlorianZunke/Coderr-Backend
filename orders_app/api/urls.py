from django.urls import path
from .views import OrdersListViewSet, OrderDetailViewSet, OrderBusinessCountView


urlpatterns = [
    path('orders/', OrdersListViewSet.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrderDetailViewSet.as_view(), name='orders-detail'),
    path('order-count/<int:pk>/', OrderBusinessCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', OrdersListViewSet.as_view(), name='completed-order-count'),
]