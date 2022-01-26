from django.urls import path, include
from django.conf.urls import include
from rest_framework import routers

from .views import (BanksAPIView, BranchesAPIView, CustomerViewSet, CustomerLoanViewSet, TransferAPIView,
                    DepositAPIView, WithdrawAPIView, CustomerReportAPIView)

app_name = 'bank'

router = routers.SimpleRouter()
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'customer_loan', CustomerLoanViewSet, basename='customer_loan')
urlpatterns = [
    path('banks/', BanksAPIView.as_view(), name='banks'),
    path('branches/', BranchesAPIView.as_view(), name='branches'),
    path('transfer/<int:id>/', TransferAPIView.as_view(), name='transaction'),
    path('deposit/<int:id>/', DepositAPIView.as_view(), name='deposit'),
    path('withdraw/<int:id>/', WithdrawAPIView.as_view(), name='withdraw'),
    path('report/<str:username>/', CustomerReportAPIView.as_view(), name='report'),
    path(r'', include(router.urls)),
]
