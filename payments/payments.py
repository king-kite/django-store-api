import json
import requests
import secrets
from django.conf import settings
from .models import Payment

PAYSTACK_BASE_END_POINT = "https://api.paystack.co"
PAYSTACK_PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PAYSTACK_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + PAYSTACK_SECRET_KEY
}

def generate_reference():
    generated_reference = None
    while not generated_reference:
        reference = secrets.token_urlsafe(50)
        object_with_similar_reference = Payment.objects.filter(
            reference=reference
        )
        if not object_with_similar_reference:
            generated_reference=reference
    return generated_reference

class PayStack():
    def __init__(self, email, amount, reference=None):
        self.email = email
        self.amount = int(amount * 100)
        self.reference = reference

    def _handle_request(self, method, url, data=None):
        payload = json.dumps(data) if data else data

        response = requests.request(method, url, headers=PAYSTACK_HEADERS, data=payload, verify=True)
        return self._handle_response(response)

    def _handle_response(self, parsed_response):
        response = parsed_response.json()
        status_code = parsed_response.status_code
        status = response.get('status', None)
        message = response.get('message', None)
        data = response.get('data', None)
        errors = response.get('errors', None)

        if parsed_response.status_code == 404:
            if not message:
                message = "The Requested Object Could Not Be Found"

        return status_code, status, message, data, errors

    def initialize(self):
        url = PAYSTACK_BASE_END_POINT + "/transaction/initialize"
        method = "POST"
        data = {
            "email": self.email,
            "amount": self.amount
        }

        if self.reference:
            data.update({"reference": self.reference})
        else:
            reference = generate_reference()
            if reference:
                data.update({"reference": reference})
                self.reference = reference

        return self._handle_request(method, url, data)

    def verify(self):
        url = PAYSTACK_BASE_END_POINT + f'/transaction/verify/{self.reference}'
        method = "GET"

        return self._handle_request(method, url)
