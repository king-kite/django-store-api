from django.db import DataError
from ..models import CartItem, Order
from .test_setup import TestSetUp

""" CartItem Model Tests """
class CartItemModelTests(TestSetUp):

    def test_create_cartitem_for_an_inactive_product(self):
        """Return DataError if an inactive product is added to Cart"""

        with self.assertRaises(DataError):
            CartItem.objects.create(
                user=self.user1, product=self.product2, quantity=1
            )

    def test_create_cartitem_for_an_active_product(self):
        cartitem = CartItem.objects.create(
            user=self.user1, product=self.product1
        )

        self.assertEqual(cartitem.quantity, 1)
        self.assertEqual(cartitem.get_total_product_price(), 100)
        self.assertEqual(cartitem.get_total_discount_product_price(), 0)
        self.assertFalse(cartitem.ordered)

    def test_original_price_final_price_and_total_discount(self):
        """ Test to get CartItem original and final price and toal discount """

        cartitem1 = CartItem.objects.create(
            user=self.user2, product=self.product1, quantity=4
        )
        cartitem2 = CartItem.objects.create(
            user=self.user2, product=self.product3, quantity=2
        )
        original_price = CartItem.objects.get_original_price(self.user2)
        final_price = CartItem.objects.get_final_price(self.user2)
        total_discount = CartItem.objects.get_total_discount(self.user2)

        self.assertEqual(cartitem2.get_total_product_price(), 600)
        self.assertEqual(cartitem2.get_total_discount_product_price(), 500)
        self.assertEqual(original_price, 1000)
        self.assertEqual(final_price, 900)
        self.assertEqual(total_discount, 100)


"""Order Model Tests"""
class OrderModelTests(TestSetUp):

    def test_do_not_create_order_on_cartitem_ordered_create(self):
        """ Test the order signal to not create an order on cart item ordered creation """

        cartitem1 = CartItem.objects.create(
            user=self.user2, product=self.product1, quantity=4, ordered=True
        )

        order = Order.objects.filter(user=self.user2).first()
        
        self.assertIsNone(order)

    def test_create_order_on_cartitem_unordered_create(self):
        """ Test the order signal to create an order on cart item unordered creation """

        cartitem1 = CartItem.objects.create(
            user=self.user2, product=self.product1, quantity=4
        )
        cartitem2 = CartItem.objects.create(
            user=self.user2, product=self.product3, quantity=2
        )

        final_price = CartItem.objects.get_final_price(self.user2)

        order = Order.objects.get(user=self.user2, ordered=False)
        order_total = order.get_total()

        self.assertEqual(final_price, order_total)
        self.assertEqual(order.status, 'UO')
        self.assertEqual(order.products.count(), 2)
        self.assertFalse(order.ordered)

    def test_order_and_cartitem_ordered(self):
        """Test to check if when ordered is True, all cart items are ordered"""

        cartitem1 = CartItem.objects.create(
            user=self.user2, product=self.product1, quantity=4
        )
        cartitem2 = CartItem.objects.create(
            user=self.user2, product=self.product3, quantity=2
        )

        order = Order.objects.get(user=self.user2, ordered=False)

        order.ordered = True
        order.save()

        cartitems = CartItem.objects.filter(user=self.user2)
        for item in cartitems:
            self.assertTrue(item.ordered)


    def test_order_and_cartitem_unordered(self):
        """Test to check if when ordered is False, all cart items are not ordered"""

        cartitem1 = CartItem.objects.create(
            user=self.user1, product=self.product1, quantity=4
        )
        cartitem2 = CartItem.objects.create(
            user=self.user1, product=self.product3, quantity=2
        )

        order = Order.objects.get(user=self.user1, ordered=False)

        order.ordered = False
        order.save()

        cartitems = CartItem.objects.filter(user=self.user1)
        for item in cartitems:
            self.assertFalse(item.ordered)
