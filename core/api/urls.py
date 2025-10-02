from django.urls import path

from core.api.views import StatisticsView


urlpatterns = [
    path('base-info/', StatisticsView.as_view(), name='base-info'),
]
