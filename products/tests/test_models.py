from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from ..models import Product, Review

User = get_user_model()


""" Product Model Tests """
class ProductModelTests(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            title="First Product",
            slug="first-product",
            description="First Product Description",
            price=800
        )

        self.assertTrue(product.is_active)

    def test_product_unique_title(self):
        product1 = Product.objects.create(
            title="First Product",
            slug="first-product",
            description="First Product Description",
            price=800
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                title="First Product",
                slug="first-product-slug",
                description="First Product Description",
                price=800
            )

    def test_product_unique_slug(self):
        product1 = Product.objects.create(
            title="First Product",
            slug="first-product",
            description="First Product Description",
            price=800
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                title="First Product Slug",
                slug="first-product",
                description="First Product Description",
                price=800
            )


""" Review Model Tests """
class ReviewModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="jon@smith.io", password="Password12345"
        )
        self.user2 = User.objects.create(
            email="Wayne@smith.io", password="Olaere4943"
        )
        self.product = Product.objects.create(
            title="First Product", slug="first-product",
            description="First Product Description", price=800
        )

    def test_review_creation(self):
        review1 = Review.objects.create(
            author=self.user, product=self.product,
            body="This is product Body", rating="5"
        )

        self.assertFalse(review1.is_approved)
        with self.assertRaises(ValueError):
            Review.objects.create(author=self.user2, product=self.product)

    def test_unique_review_for_author(self):
        review = Review.objects.create(
            author=self.user, product=self.product,
            body="This is product Body", rating="5"
        )
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                author=self.user, product=self.product,
                body="This is product Body", rating="5"
            )
