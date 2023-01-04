from django.urls import include, path
from .views import ProductDetailView, ProductListView, ReviewDetailView, ReviewListView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/reviews/<slug>/', ReviewListView.as_view(), name='reviews'),
    path('product/review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
