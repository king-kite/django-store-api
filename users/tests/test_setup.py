from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class TestSetUp(APITestCase):

    def setUp(self):
        """ Initialise Variables """
        self.client = APIClient()
        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.user_data_url = reverse('rest_user_details')
        self.register_url = reverse('rest_register')
        self.change_password_url = reverse('rest_password_change')
        self.reset_password_url = reverse('rest_password_reset')
        self.reset_password_confirm_url = reverse('rest_password_reset_confirm')
        # Test for email verification rest_verify_email

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
