from django_countries.data import COUNTRIES
from rest_framework import serializers
from users.models import Address
from users.serializers import AddressSerializer
from .models import CartItem, Order


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user')
        product = validated_data.get('product')
        raw_quantity = validated_data.get('quantity')

        if raw_quantity:
            quantity = int(raw_quantity)
        else:
            quantity = 1

        cart_item_queryset = CartItem.objects.filter(user=user, product=product, ordered=False)

        if cart_item_queryset.exists():
            cart_item = cart_item_queryset.first()
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(user=user, product=product, quantity=quantity)
        return cart_item


class CheckoutSerializer(serializers.Serializer):
    default_billing_address = serializers.SerializerMethodField('get_default_billing')
    default_shipping_address = serializers.SerializerMethodField('get_default_shipping')
    countries = serializers.SerializerMethodField('get_all_countries')

    def get_all_countries(self, obj):
        return COUNTRIES

    def get_default_billing(self, obj):
        user = self.context.get('user')
        address = Address.objects.check_default_address(user, 'B')
        if address:
            serializer = AddressSerializer(address)
            return serializer.data
        return None

    def get_default_shipping(self, obj):
        user = self.context.get('user')
        address = Address.objects.check_default_address(user, 'S')
        if address:
            serializer = AddressSerializer(address)
            return serializer.data
        return None


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'products', 'ordered', 'status', 'billing_address', 'shipping_address', 'date_updated')
