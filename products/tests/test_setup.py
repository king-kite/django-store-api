from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from ..models import Product, Review

User = get_user_model()


class TestSetUp(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')
        self.product_list_url = reverse('products')

        self.user = User.objects.create(email="walter@white.io")
        self.user.set_password("Passing1234")
        self.user.save()

        self.product1 = Product.objects.create(
            title="Product One", slug="product-one",
            description="Product One Description", price=100)

        self.product2 = Product.objects.create(
            title="Product Two", slug="product-two",
            description="Product Two Description", price=200, is_active=False)

        self.product3 = Product.objects.create(
            title="Product Three", slug="product-three",
            description="Product Three Description", price=300, discount_price=250)

        self.product4 = Product.objects.create(
            title="Product Four", slug="product-four",
            description="Product Four Description", price=300, discount_price=250)

        self.review = Review.objects.create(author=self.user, product=self.product4,
            body="This is a Review on Product One", rating="5")

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
