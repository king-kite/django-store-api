from django.contrib.auth import get_user_model
# from django.core import mail
from rest_framework.authtoken.models import Token
from .test_setup import TestSetUp

User = get_user_model()


""" Registration Tests """
class RegistrationTests(TestSetUp):
	""" Test the functionality of the Registration API """

	def test_registration(self):
		"""Test registration"""

		response = self.client.post(self.register_url, {
			"email": "Jon@Wayne.com",
			"password1": "Response2000",
			"password2": "Response2000",
		})

		user = User.objects.get(email="Jon@Wayne.com")
		token = Token.objects.get(user=user)

		self.assertEqual(response.status_code, 201)
		self.assertIsNotNone(user)
		self.assertIsNotNone(token)
		self.assertTrue(user.check_password('Response2000'))
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_admin)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)


""" Login Tests """
class LoginTests(TestSetUp):
	""" Test the functionality of the Login API """

	def test_basic_login(self):
		"""Test login"""

		user = User.objects.create(email="john@smith.io")
		user.set_password("Response12345")
		user.save()

		response1 = self.client.post(self.login_url, {
			"email": "john@smith.io", "password": "Response12345" }, format="json")

		response2 = self.client.login(email="john@smith.io", password="Response12345")

		response3 = self.client.post(self.logout_url, {})

		self.assertEqual(response1.status_code, 200)
		self.assertEqual(response3.status_code, 200)
		self.assertTrue(response2)
		self.assertTrue(user.is_authenticated)
		self.assertIsNotNone(response1.data['key'])

	def test_inactive_login(self):
		"""Test Failed Login For Inactive Users"""

		wayne = User.objects.create(email="wayne@smith.io")
		wayne.set_password("Response12345")
		wayne.is_active = False
		wayne.save()

		response1 = self.client.post(self.login_url, {
			"email": "wayne@smith.io", "password": "Response12345" }, format="json")

		response2 = self.client.login(email=wayne.email, password="Response12345")

		response3 = self.client.post(self.logout_url, {})

		self.assertEqual(response1.status_code, 400)
		self.assertEqual(response3.status_code, 200)
		self.assertFalse(response2)
		with self.assertRaises(KeyError):
			token_key = response1.data['key']


""" User Data Tests"""
class UserDataTests(TestSetUp):
    """ Test the functionality of the User Data API """

    def test_get_user_data_without_authentication(self):
        response = self.client.get(self.user_data_url)
        self.assertEqual(response.status_code, 403)

    def test_get_user_data_with_authentication(self):
        self.client.post(self.register_url, {
            "email": "bar@bie.com","password1": "Same0000","password2":"Same0000"
        })
        response = self.client.get(self.user_data_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], "bar@bie.com")


""" Password Reset Tests"""
class PasswordReset(TestSetUp):
	
	def test_reset_password(self):
		response = self.client.post(self.reset_password_url, {
			"email": "Jon@Wayne.com",
		})

		self.assertEqual(response.status_code, 200)


""" Password Change Tests """
class PasswordChangeTest(TestSetUp):
	
	def test_change_password_by_unauthenticated_user(self):
		""" Test to check if the user is not authenticated """

		user = User.objects.create(email="myman@example.com")
		user.set_password('Passing1234')
		user.save()

		response = self.client.post(self.change_password_url, {
			"old_password": "Passing1234",
			"new_password1": "Password1234",
			"new_password2": "Password1234"
		})

		self.assertEqual(response.status_code, 403)

	def test_change_password_by_authenticated_user(self):
		""" Test to change password for an authenticated user """

		self.client.post(self.register_url, {
			"email": "mrman@example.com",
			"password1": "Passing1234",
			"password2": "Passing1234"
		})

		response = self.client.post(self.change_password_url, {
			"old_password": "Passing1234",
			"new_password1": "PassTheGameHere1234",
			"new_password2": "PassTheGameHere1234"
		})

		mrman = User.objects.get(email="mrman@example.com")

		self.assertEqual(response.status_code, 200)
		self.assertTrue(mrman.check_password("PassTheGameHere1234"))

		