import json
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.db import IntegrityError
from django.urls import reverse
from ..models import Review
from .test_setup import TestSetUp

User = get_user_model()


""" Product List View Tests """
class ProductListViewTests(TestSetUp):

    def test_get_products(self):
        """ Test to return only active products """
        response = self.client.get(self.product_list_url)
        content = response.content
        data = json.loads(content.decode('utf-8'))
        product1 = data[0]
        product3 = data[1]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(product1['title'], self.product1.title)
        self.assertEqual(product1['slug'], self.product1.slug)
        self.assertEqual(product1['price'], self.product1.price)

        self.assertEqual(product3['title'], self.product3.title)
        self.assertEqual(product3['price'], self.product3.price)
        self.assertEqual(product3['slug'], self.product3.slug)

    def test_post_products(self):
        """ Return Method Not Allowed """
        response = self.client.post(self.product_list_url, {})
        self.assertEqual(response.status_code, 405)


""" Product Detail View Tests """
class ProductDetailViewTests(TestSetUp):

    def test_get_product(self):
        """ Test to return only active product """
        response1 = self.client.get(self.product1.get_absolute_url())
        response2 = self.client.get(self.product2.get_absolute_url())
        response3 = self.client.get(self.product3.get_absolute_url())

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response3.status_code, 200)

        self.assertEqual(response1.data['title'], self.product1.title)
        self.assertEqual(response3.data['title'], self.product3.title)
        self.assertIsNone(response2.data)

    def test_put_and_delete_product(self):
        """ Return Method Not Allowed """
        response1 = self.client.put(self.product1.get_absolute_url(), {})
        response2 = self.client.delete(self.product3.get_absolute_url(), {})

        self.assertEqual(response1.status_code, 405)
        self.assertEqual(response2.status_code, 405)


""" Revew List View Tests """
class ReviewListViewTests(TestSetUp):

    def test_get_all_active_reviews(self):
        """ Test to get the reviews of an active Product """

        response1 = self.client.get(self.product4.get_reviews_url())
        response2 = self.client.get(self.product2.get_reviews_url())

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)

    def test_create_review_without_authentication(self):

        response = self.client.post(self.product1.get_reviews_url(), {
            "author": self.user.id, "product": self.product1.id, "rating": "4",
            "body": f"This is {self.user.email.capitalize()} Review For Product 1"
        }, format="json")

        self.assertEqual(response.status_code, 401)

    def test_create_review_with_authentication(self):

        self.client.post(self.login_url, {
            "email": self.user.email, "password": "Passing1234" }, format="json")

        response1 = self.client.post(self.product1.get_reviews_url(), {
            "author": self.user.id, "product": self.product1.id, "rating": "4",
            "body": f"This is {self.user.email.capitalize()} Review For Product 1"
        }, format="json")

        response3 = self.client.post(self.product3.get_reviews_url(), {
            "author": self.user.id, "product": self.product3.id,
            "body": f"This is {self.user.email.capitalize()} Review For Product 3"
        }, format="json")

        review = Review.objects.get(author=self.user, product=self.product3)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response3.data['rating'], review.rating)
        self.assertEqual(review.rating, "5")

        with self.assertRaises(FieldError):
            self.client.post(self.product2.get_reviews_url(), {
                "author": self.user.id, "product": self.product2.id, "rating": "4",
                "body": f"This is {self.user.email.capitalize()} Review For Product 2"
            }, format="json")

    def test_unique_review_for_author(self):
        """ Test to check that each user only has a single review for a product """

        res = self.client.post(self.login_url, {
            "email": self.user.email, "password": "Passing1234" }, format="json")

        response1 = self.client.post(self.product3.get_reviews_url(), {
            "author": self.user.id, "product": self.product3.id, "rating": "4",
            "body": f"This is {self.user.email.capitalize()} Review For Product 3"
        }, format="json")

        response2 = self.client.post(self.product3.get_reviews_url(), {
            "author": self.user.id, "product": self.product3.id, "rating": "4",
            "body": f"This is {self.user.email.capitalize()} Review For Product 3"
        }, format="json")

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)

    def test_authenticated_user_cannot_create_review_for_another_user(self):
        """ Test to confirm that an authenticated user cannot create a review for another user """

        user = self.client.post(self.register_url, {
            "email": "jenny@fer.io", "password1": "Authen4321", "password2": "Authen4321"
        }, format="json")

        response1 = self.client.post(self.product1.get_reviews_url(), {
            "author": self.user.id, "product": self.product1.id, "rating": "4",
            "body": f"This is {self.user.email.capitalize()} Review For Product 1"
        }, format="json")

        self.assertEqual(response1.status_code, 401)


""" Review Detail Get View Tests """
class ReviewDetailGetViewTests(TestSetUp):
    """ Test the get method on the Review Detail View """

    def test_get_single_review_by_anonymous_user(self):
        """ Return Unauthorized if the request user is anonymous """

        response = self.client.get(self.review.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_get_single_review_by_unauthorized_user(self):
        """ Return Unauthorized if the request user is not the author of the review """
        self.client.post(self.register_url, {
            "email": "amanda@wall.is", "password1": "PassGame1", "password2": "PassGame1"
        }, format="json")

        response = self.client.get(self.review.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_get_single_review_by_authorized_user(self):
        self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.review.get_absolute_url())

        self.assertEqual(response.status_code, 200)


""" Review Detail Put View Tests """
class ReviewDetailPutViewTests(TestSetUp):
    """ Test the put method on the Review Detail View """

    def test_put_review_by_anonymous_user(self):
        """ Return Unauthorized if the request user is anonymous """

        response = self.client.put(self.review.get_absolute_url(), {
            "author": 1, "product": 4, "body": "Updated Product 4 Review", "rating": "4"
        })

        self.assertEqual(response.status_code, 401)

    def test_put_review_by_unauthorized_user(self):
        """ Return Unauthorized if the request user is not the author of the review """

        self.client.post(self.register_url, {
            "email": "ama@wall.is", "password1": "PassGame1", "password2": "PassGame1"
        }, format="json")

        response = self.client.put(self.review.get_absolute_url(), {
            "author": 1, "product": 4, "body": "Updated Product 4 Review", "rating": "4"
        })

        self.assertEqual(response.status_code, 401)

    def test_put_review_by_authorized_user(self):
        self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "Passing1234"
        }, format="json")

        response = self.client.put(self.review.get_absolute_url(), {
            "author": 1, "product": 4, "body": "Updated Product 4 Review", "rating": "4"
        })

        review = Review.objects.get(id=int(response.data['id']))

        self.assertIsNotNone(review)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['body'], review.body)
        self.assertEqual(response.data['rating'], review.rating)
        self.assertEqual(response.data['product'], review.product.id)
        self.assertEqual(response.data['author'], review.author.id)


""" Review Detail Delete View Tests """
class ReviewDetailDeleteViewTests(TestSetUp):
    """ Test the delete method on the Review Detail View """

    def test_delete_review_by_anonymous_user(self):
        """ Return Unauthorized if the request user is anonymous """

        response = self.client.delete(self.review.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_delete_review_by_unauthorized_user(self):
        """ Return Unauthorized if the request user is not the author of the review """

        self.client.post(self.register_url, {
            "email": "mana@wall.is", "password1": "PassGame1", "password2": "PassGame1"
        }, format="json")

        response = self.client.delete(self.review.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_delete_review_by_authorized_user(self):
        self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "Passing1234"
        }, format="json")

        response = self.client.delete(self.review.get_absolute_url())

        review = Review.objects.filter(id=self.review.id).first()

        self.assertIsNone(review)
        self.assertEqual(response.status_code, 204)
