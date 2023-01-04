from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from products.models import Product
from orders.models import CartItem, Order
from ..models import Payment

User = get_user_model()

"""Payment Test"""
class PaymentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="jeffrey@jimmy.jill")
        self.user.set_password('Passing1234')
        self.user.save()

        self.product1 = Product.objects.create(
            title="Product One", slug="product-one",
            description="Product One Description", price=100)

        self.product2 = Product.objects.create(
            title="Product Two", slug="product-two",
            description="Product Two Description", price=300)

        self.cartitem1 = CartItem.objects.create(
            user=self.user, product=self.product1, quantity=4
        )

        self.cartitem2 = CartItem.objects.create(
            user=self.user, product=self.product2, quantity=2
        )

        self.order = Order.objects.get(user=self.user, ordered=False)

    def test_create_payment(self):
        reference = "4ht498343$#$684898Y&(#&@J@K)?>>?23>#32r!"
        payment_method = 'P'

        payment = Payment.objects.create(user=self.user, order_id=self.order.id,
            reference=reference, payment_method='P', amount=self.order.get_total()
        )

        with self.assertRaises(IntegrityError):
            Payment.objects.create(user=self.user, order_id=self.order.id,
                reference=reference, payment_method='P', amount=self.order.get_total()
            )

    def test_sentinel_user(self):
        user = User.objects.create(email="sdk@java.java")
        reference = "4ht498343$#$684e5898Y&(#&@J@K)?>>?23>#32r!"
        payment_method = 'P'

        payment = Payment.objects.create(user=user, order_id=self.order.id,
            reference=reference, payment_method='P', amount=self.order.get_total()
        )

        user.delete()

        new_payment = Payment.objects.get(id=payment.id)

        s_user = User.objects.get(email="deleted_user@paymentapp.py")

        self.assertEqual(new_payment.user, s_user)
