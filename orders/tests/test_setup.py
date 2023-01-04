from django.contrib.auth import get_user_model
from django.urls import reverse
from orders.models import CartItem, Order
from products.models import Product
from rest_framework.test import APIClient, APITestCase
from users.models import Address

User = get_user_model()


class TestSetUp(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.cart_url = reverse('cart')
        self.checkout_url = reverse('checkout')
        self.login_url = reverse('rest_login')

        self.user1 = User.objects.create(email="walter@white.io")
        self.user1.set_password("Passing1234")
        self.user1.save()

        self.user2 = User.objects.create(email="jenny@philip.io")
        self.user2.set_password("Passing1234")
        self.user2.save()

        self.user3 = User.objects.create(email="jerry@philip.io")
        self.user3.set_password("Passing1234")
        self.user3.save()

        self.user4 = User.objects.create(email="april@may.june")
        self.user4.set_password("Passing1234")
        self.user4.save()

        self.user5 = User.objects.create(email="jason@comet.man")
        self.user5.set_password("Passing1234")
        self.user5.save()

        self.user6 = User.objects.create(email="mary@jane.girl")
        self.user6.set_password("Passing1234")
        self.user6.save()

        self.product1 = Product.objects.create(
            title="Product One", slug="product-one",
            description="Product One Description", price=100)

        self.product2 = Product.objects.create(
            title="Product Two", slug="product-two",
            description="Product Two Description", price=200, is_active=False)

        self.product3 = Product.objects.create(
            title="Product Three", slug="product-three",
            description="Product Three Description", price=300, discount_price=250)

        self.cartitem1 = CartItem.objects.create(
            user=self.user3, product=self.product1, quantity=4
        )

        self.cartitem2 = CartItem.objects.create(
            user=self.user3, product=self.product3, quantity=2
        )

        self.cartitem3 = CartItem.objects.create(
            user=self.user3, product=self.product3, quantity=1, ordered=True
        )

        self.cartitem4 = CartItem.objects.create(
            user=self.user4, product=self.product1, quantity=6
        )

        self.cartitem5 = CartItem.objects.create(
            user=self.user4, product=self.product3, quantity=4
        )

        self.cartitem6 = CartItem.objects.create(
            user=self.user5, product=self.product3, quantity=3
        )

        self.cartitem7 = CartItem.objects.create(
            user=self.user6, product=self.product3, quantity=3
        )

        self.billing_address =  {
            "address1": "This is Billing Address 1",
            "address2": "This is Billing Address 2",
            "country": "NG",
            "state": "Billing State",
            "city": "Billing City",
            "zipcode": "Billing Zippy",
         }

        self.shipping_address =  {
            "address1": "This is Shipping Address 1",
            "address2": "This is Shipping Address 2",
            "country": "NG",
            "state": "Shipping State",
            "city": "Shipping City",
            "zipcode": "Shipping Zippy",
         }

        self.user4_billing_address = Address.objects.create(
            user=self.user4, address_type='B', default=True, **self.billing_address)
        self.user4_shipping_address = Address.objects.create(
            user=self.user4, address_type='S', default=True, **self.shipping_address)

        self.user5_billing_address = Address.objects.create(
            user=self.user5, address_type='B', default=True, **self.billing_address)

        self.user6_shipping_address = Address.objects.create(
            user=self.user6, address_type='S', default=True, **self.shipping_address)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
