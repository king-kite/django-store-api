from orders.models import CartItem, Order
from users.models import Address
from .test_setup import TestSetUp


"""CartItem List View Tests"""
class CartItemListViewTests(TestSetUp):

    def test_get_cart_list_by_unauthenticated_user(self):
        """ Return UnAuthenticated """

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, 401)

    def test_get_cart_list_by_authenticated_user(self):

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, 200)

    def test_post_cart_list_by_unauthenticated_user(self):
        """ Return UnAuthenticated """

        response = self.client.post(self.cart_url, {})

        self.assertEqual(response.status_code, 401)

    def test_post_cart_list_by_authenticated_user_to_an_inactive_product(self):
        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.post(self.cart_url, {
            "user": self.user1.id,
            "product": self.product2.id,
        })

        cartitem = CartItem.objects.filter(user=self.user1, product=self.product2).first()

        self.assertEqual(response.status_code, 404)
        self.assertIsNone(cartitem)

    def test_post_cart_list_by_authenticated_user_to_an_active_product(self):
        self.client.post(self.login_url, {
            "email": self.user2.email, "password": "Passing1234"
        }, format="json")

        response = self.client.post(self.cart_url, {
            "user": self.user2.id,
            "product": self.product1.id,
        })

        cartitem = CartItem.objects.get(user=self.user2, product=self.product1)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(cartitem.quantity, 1)
        self.assertFalse(cartitem.ordered)

    def test_add_to_an_existing_cartitem(self):
        """ Test to check if the quantity adds to existing cart quantity """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.post(self.cart_url, {
            "user": self.user3.id, "product": self.product1.id, "quantity": 5
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user3.id)
        self.assertEqual(response.data['product'], self.product1.id)
        self.assertEqual(response.data['quantity'], 9)
        self.assertFalse(response.data['ordered'])


"""CartItem Detail Get View Tests"""
class CartItemDetailGetViewTests(TestSetUp):
    def test_get_cart_item_by_unauthenticated_user(self):
        """ Return UnAuthenticated """

        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, 401)

    def test_get_cart_item_by_authenticated_user_but_unauthorized(self):
        """ Test to check that an authenticated user can't get another user's cart item """

        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.cartitem1.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_get_cart_item_by_authenticated_and_authorized_user(self):
        """ Test to check that an authenticated user can get his cart item """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.cartitem1.get_absolute_url())

        self.assertEqual(response.status_code, 200)


"""CartItem Detail Put View Tests"""
class CartItemDetailPutViewTests(TestSetUp):
    def test_put_cart_item_by_unauthenticated_user(self):
        """ Return UnAuthenticated """

        response = self.client.put(self.cart_url, {})

        self.assertEqual(response.status_code, 401)

    def test_put_cart_item_by_authenticated_user_but_unauthorized(self):
        """ Test to check that an authenticated user can't put another user's cart item """

        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.put(self.cartitem1.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product3.id,
            "quantity": 6
        })

        self.assertEqual(response.status_code, 401)

    def test_put_cart_item_by_authenticated_user_and_authorized_user_to_active_product(self):
        """ Test to check that an authenticated user can put in his cart """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.put(self.cartitem2.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product3.id,
            "quantity": 6
        })

        cartitem = CartItem.objects.get(id=self.cartitem2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cartitem.quantity, 6)
        self.assertFalse(cartitem.ordered)

    def test_put_cart_item_by_authenticated_user_and_authorized_user_to_inactive_product(self):
        """ Test to check that an authenticated user cannot put an inactive product in his cart """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.put(self.cartitem2.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product2.id,
            "quantity": 6
        })

        cartitem = CartItem.objects.get(id=self.cartitem2.id)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(cartitem.quantity, 2)
        self.assertFalse(cartitem.ordered)

    def test_put_cart_item_check_the_right_product_for_cart_item(self):
        """ Test to check that the right product is being put in the cart """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.put(self.cartitem2.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product1.id,
            "quantity": 12
        })

        cartitem1 = CartItem.objects.get(id=self.cartitem1.id)
        cartitem2 = CartItem.objects.get(id=self.cartitem2.id)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(cartitem1.quantity, 4)
        self.assertEqual(cartitem2.quantity, 2)
        self.assertFalse(cartitem2.ordered)
        self.assertFalse(cartitem2.ordered)

    def test_put_cart_item_deletes_when_quantity_is_less_than_or_equal_ZERO(self):
        """Test to check that a cartitem deletes when the quantity is less than or equal to zero"""

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response1 = self.client.put(self.cartitem1.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product1.id,
            "quantity": 0
        })

        response2 = self.client.put(self.cartitem2.get_absolute_url(), {
            "user": self.user3.id,
            "product": self.product3.id,
            "quantity": -5
        })

        cartitem1 = CartItem.objects.filter(id=self.cartitem1.id).first()
        cartitem2 = CartItem.objects.filter(id=self.cartitem2.id).first()

        order = Order.objects.filter(user=self.user3).first()

        self.assertEqual(response1.status_code, 204)
        self.assertEqual(response2.status_code, 204)
        self.assertIsNone(cartitem1)
        self.assertIsNone(cartitem2)
        self.assertIsNone(order)


"""CartItem Detail Delete View Tests"""
class CartItemDetailDeleteViewTests(TestSetUp):
    def test_delete_cart_item_by_unauthenticated_user(self):
        """ Return UnAuthenticated """

        response = self.client.delete(self.cart_url)

        self.assertEqual(response.status_code, 401)

    def test_delete_cart_item_by_authenticated_user_but_unauthorized(self):
        """ Test to check that an authenticated user cannot delete another user's cart item """

        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.delete(self.cartitem1.get_absolute_url())

        self.assertEqual(response.status_code, 401)

    def test_delete_cart_item_by_authenticated_and_authorized_user(self):
        """ Test to check that an authenticated and authorized user can delete his cart item """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.delete(self.cartitem1.get_absolute_url())

        cartitem = CartItem.objects.filter(id=self.cartitem1.id).first()
        order = Order.objects.get(user=self.user3, ordered=False)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(order.products.count(), 1)
        self.assertIsNone(cartitem)


"""Checkout View Get Tests"""
class CheckoutViewGetTests(TestSetUp):

    def test_get_data_by_unauthenticated_user(self):
        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 401)

    def test_get_data_by_authenticated_user_but_no_order(self):
        """Return 404 because this user has no item in his cart"""

        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 404)

    def test_get_data_by_authenticated_user_with_order(self):
        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['countries'])

    def test_get_data_by_authenticated_user_with_order_but_no_default_address(self):
        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['default_billing_address'])
        self.assertIsNone(response.data['default_shipping_address'])

    def test_get_data_by_authenticated_user_with_order_and_default_address(self):
        self.client.post(self.login_url, {
            "email": self.user4.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['default_billing_address'])
        self.assertIsNotNone(response.data['default_shipping_address'])

    def test_get_data_by_authenticated_user_with_order_and_billing_address(self):
        """Test to check that the user only has a billing address"""

        self.client.post(self.login_url, {
            "email": self.user5.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['default_billing_address'])
        self.assertIsNone(response.data['default_shipping_address'])

    def test_get_data_by_authenticated_user_with_order_and_shipping_address(self):
        """Test to check that the user only has a shipping address"""

        self.client.post(self.login_url, {
            "email": self.user6.email, "password": "Passing1234"
        }, format="json")

        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['default_shipping_address'])
        self.assertIsNone(response.data['default_billing_address'])


"""Checkout View Post Tests"""
class CheckoutViewPostTests(TestSetUp):

    def test_post_data_by_unauthenticated_user(self):
        response = self.client.post(self.checkout_url, {})

        self.assertEqual(response.status_code, 401)

    def test_post_data_by_authenticated_user_but_no_order(self):
        """Return 404 because this user has no item in his cart"""

        self.client.post(self.login_url, {
            "email": self.user1.email, "password": "Passing1234"
        }, format="json")

        response = self.client.post(self.checkout_url, {})

        self.assertEqual(response.status_code, 404)

    def test_post_data_by_authenticated_user_with_default_address_false(self):
        """ Test to check that the default address sent is false """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        billing_address = self.billing_address.copy();billing_address.update({'default': False})
        shipping_address = self.shipping_address.copy();shipping_address.update({'default': False})

        response = self.client.post(self.checkout_url, {
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "same_address": False,
        }, format="json")

        billing_address = Address.objects.get(user=self.user3, address_type='B')
        shipping_address = Address.objects.get(user=self.user3, address_type='S')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(billing_address)
        self.assertIsNotNone(shipping_address)
        self.assertFalse(billing_address.default)
        self.assertFalse(shipping_address.default)

    def test_post_data_by_authenticated_user_with_default_address(self):
        """ Test to check that the default address sent is true """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        billing_address = self.billing_address.copy();billing_address.update({'default': True})
        shipping_address = self.shipping_address.copy();shipping_address.update({'default': True})

        response = self.client.post(self.checkout_url, {
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "same_address": False,
        }, format="json")

        address = Address.objects.filter(user=self.user3)
        billing_address = Address.objects.get(user=self.user3, address_type='B')
        shipping_address = Address.objects.get(user=self.user3, address_type='S')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(billing_address)
        self.assertIsNotNone(shipping_address)
        self.assertTrue(billing_address.default)
        self.assertTrue(shipping_address.default)

    def test_post_data_by_authenticated_user_with_no_address(self):
        """ Test to check that no address gives 400 BAD REQUEST """
        # Return 400 BAD REQUEST

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        response = self.client.post(self.checkout_url, {}, format="json")

        billing_address = Address.objects.filter(user=self.user3, address_type='B').first()
        shipping_address = Address.objects.filter(user=self.user3, address_type='S').first()

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(billing_address)
        self.assertIsNone(shipping_address)

    def test_post_data_only_billing_address_and_no_same_address(self):
        """ Test to check that only billing address without same address """
        # Return 400 BAD REQUEST

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        billing_address = self.billing_address.copy();billing_address.update({'default': False})

        response = self.client.post(self.checkout_url, {
            "billing_address": billing_address,
            "same_address": False,
        }, format="json")

        shipping_address = Address.objects.filter(user=self.user3, address_type='S').first()

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(shipping_address)

    def test_post_data_only_billing_address_and_same_address(self):
        """ Test to check only billing address with same address """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        billing_address = self.billing_address.copy();billing_address.update({'default': True})

        response = self.client.post(self.checkout_url, {
            "billing_address": billing_address,
            "same_address": True,
        }, format="json")

        shipping_address = Address.objects.get(user=self.user3, address_type='S')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(shipping_address)
        self.assertTrue(shipping_address.default)

    def test_post_data_only_shipping_address_and_no_same_address(self):
        """ Test to check that only shipping address without same address """
        # Return 400 BAD REQUEST

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        shipping_address = self.billing_address.copy();shipping_address.update({'default': True})

        response = self.client.post(self.checkout_url, {
            "shipping_address": shipping_address,
            "same_address": False,
        }, format="json")

        billing_address = Address.objects.filter(user=self.user3, address_type='B').first()

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(billing_address)

    def test_post_data_only_shipping_address_and_same_address(self):
        """ Test to check only shipping address with same address """

        self.client.post(self.login_url, {
            "email": self.user3.email, "password": "Passing1234"
        }, format="json")

        shipping_address = self.billing_address.copy();shipping_address.update({'default': True})

        response = self.client.post(self.checkout_url, {
            "shipping_address": shipping_address,
            "same_address": True,
        }, format="json")

        billing_address = Address.objects.get(user=self.user3, address_type='B')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(billing_address)
        self.assertTrue(billing_address.default)
