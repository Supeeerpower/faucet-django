from django.urls import path
from .views import FundView, StatsView

urlpatterns = [
    path('fund/', FundView.as_view(), name='fund'),
    path('stats/', StatsView.as_view(), name='stats'),
]
