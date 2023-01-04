from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Address
from products.models import Product
from .models import CartItem, Order
from .serializers import CartItemSerializer, CheckoutSerializer, OrderSerializer


class CartItemListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_objects(self, user):
        try:
            cart_items = CartItem.objects.filter(user=user, ordered=False)
            return cart_items
        except CartItem.DoesNotExist:
            return None

    def get_product(self, id):
        try:
            product = Product.objects.get(id=id, is_active=True)
            return product
        except Product.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        cart_items = self.get_objects(request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.id == int(request.data['user']):
            product = self.get_product(int(request.data['product']))
            if product:
                serializer = CartItemSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'message':
            "You are not authorized to add this item to another user's cart"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class CartItemDetailView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, ordered=False)
            return cart_item
        except CartItem.DoesNotExist:
            return None

    def get_product(self, id):
        try:
            product = Product.objects.get(id=id, is_active=True)
            return product
        except Product.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        cart_item = self.get_object(kwargs['pk'])
        if cart_item:
            if cart_item.user == request.user:
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        cart_item = self.get_object(kwargs['pk'])
        product = self.get_product(request.data.get('product', None))
        if cart_item:
            if cart_item.user == request.user and request.user.id == int(request.data['user']):
                if int(request.data['quantity']) <= 0:
                    message = f'Successfully removed {cart_item.product.title} from Cart!'
                    cart_item.delete()
                    return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)

                if product is None or cart_item.product != product:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                serializer = CartItemSerializer(cart_item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object(kwargs['pk'])
        if cart_item:
            if cart_item.user == request.user:
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CheckoutView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create_address(self, address_type, data):
        address = Address.objects.create(
            user=self.request.user,
            address_type=address_type,
            **data
        )

        return address

    def get_order(self):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False).first()
            return order
        except Order.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        order = self.get_order()
        if order:
            serializer = CheckoutSerializer({}, context={'user': request.user})
            return Response(serializer.data)
        return Response({"message": "You have no items in your cart"},
            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        order = self.get_order()
        if order:
            billing = request.data.get('billing_address', None)
            shipping = request.data.get('shipping_address', None)
            same_address = request.data.get('same_address', None)

            if same_address == True:
                if shipping:
                    billing_address = self.create_address('B', shipping)
                    shipping_address = self.create_address('S', shipping)
                elif billing:
                    billing_address = self.create_address('B', billing)
                    shipping_address = self.create_address('S', billing)
                else:
                    return Response(
                        {'message': "Billing or Shipping Address is required!", 'status': False},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                if billing:
                    billing_address = self.create_address('B', billing)
                else:
                    return Response(
                        {'message': "Billing Address is required!", 'status': False},
                        status=status.HTTP_400_BAD_REQUEST)
                if shipping:
                    shipping_address = self.create_address('S', shipping)
                else:
                    return Response(
                        {'message': "Shipping Address is required!", 'status': False},
                        status=status.HTTP_400_BAD_REQUEST)

            if billing_address and shipping_address:
                order.billing_address = billing_address
                order.shipping_address = shipping_address
                order.save()
                return Response({'message': "Address has been added to Successfully!",
                    'status': True},
                    status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You have no items in your cart"},
            status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_objects(self, user):
        try:
            orders = Order.objects.filter(user=user, ordered=True)
            return orders
        except Order.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        orders = self.get_objects(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
