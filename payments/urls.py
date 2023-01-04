from django.urls import path
from .views import PaymentView, PaymentVerificationView


urlpatterns = [
    path('payments/<payment_method>/', PaymentView.as_view(), name='payment'),
    path('payment/verify/<reference>/', PaymentVerificationView.as_view(), name='verify-payment'),
]
