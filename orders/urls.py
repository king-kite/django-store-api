from django.urls import path
from .views import CartItemDetailView, CartItemListView, CheckoutView, OrderView


urlpatterns = [
    path('cart/', CartItemListView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartItemDetailView.as_view(), name='cartitem'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
]
