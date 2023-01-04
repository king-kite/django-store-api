from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order
from .models import Payment
from .payments import PayStack


PAYMENT_CHOICES = {
    'paystack': (PayStack, 'P'),
    'P': PayStack
}


class PaymentView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def create_payment(self, reference, payment_method):
        order = self.get_order()
        payment = Payment.objects.create(
            user=self.request.user,
            order_id=order.id,
            reference=reference,
            payment_method=payment_method,
            amount=order.get_total()
        )
        order.ordered = True
        order.status= 'P'
        order.payment = payment
        order.save()
        return payment

    def get_order(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return order
        except Order.DoesNotExist:
            return None

    def get_payment_system(self, method):
        payment_method = PAYMENT_CHOICES.get(method, None)
        return payment_method

    def get(self, request, *args, **kwargs):
        user = request.user
        order = self.get_order()
        payment_method = self.get_payment_system(kwargs['payment_method'])[0]
        if not order:
            return Response(
                {'message': 'You have no orders', 'status': False},
                status=HTTP_404_NOT_FOUND)
        if not payment_method:
            return Response({'message': 'Invalid Payment Method', 'status': False},
                status=HTTP_400_BAD_REQUEST)

        payment = payment_method(user.email, order.get_total());
        status_code, status, message, data, errors = payment.initialize()

        if status == True:
            payment_method = self.get_payment_system(kwargs['payment_method'])[1]
            self.create_payment(payment.reference,payment_method)

            return Response({
                'status': status,
                'message': message,
                'auth_url': data['authorization_url'],
                'reference': payment.reference,
            })
        return Response({
            'status': status,
            'message': message,
            'errors': errors
        }, status=HTTP_400_BAD_REQUEST)


class PaymentVerificationView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission = (IsAuthenticated, )

    def get_order(self, payment):
        try:
            order = Order.objects.get(payment=payment)
            return order
        except Order.DoesNotExist:
            return None

    def get_payment(self, reference):
        try:
            payment = Payment.objects.get(reference=reference)
            return payment
        except Payment.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = request.user
        reference = kwargs['reference']
        payment = self.get_payment(reference)
        order = self.get_order(payment)
        payment_method = PAYMENT_CHOICES.get(payment.payment_method, None)

        if not payment:
            return Response({'message': f'No Payment With Reference: {reference}', 'status': False},
                status=HTTP_404_NOT_FOUND)

        if not order:
            return Response({
                'message': f'Order With Payment Reference: {reference} Does Not Exist!',
                'status': False},
                status=HTTP_404_NOT_FOUND)

        if not payment_method:
            return Response({'message': 'Invalid Payment Method', 'status': False},
                status=HTTP_400_BAD_REQUEST)

        if user != order.user or user.is_admin == False:
            return Response({'message': 'You are not authorized to verify this transaction',
                'status': False},
                status=HTTP_401_UNAUTHORIZED)

        Vpayment = payment_method(payment.user.email, payment.amount, payment.reference)
        status_code, status, message, data, errors = Vpayment.verify()

        if status == True:
            amount_paid = int(data['amount']) / 100
            if payment.amount == amount_paid:
                order.ordered = True
                order.status = 'P'
                order.save()
                payment.verified = True
                payment.save()

                return Response({
                    'status': status,
                    'message': message,
                    'data': data,
                }, status=HTTP_200_OK)
            return Response({
                'status': False,
                'message': f'The Amount paid: {amount_paid} does not match the order payment: {payment.amount}'
            })
        return Response({
            'status': status,
            'message': message,
            'errors': errors
        }, status=HTTP_400_BAD_REQUEST)
