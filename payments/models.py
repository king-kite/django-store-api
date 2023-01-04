from django.contrib.auth import get_user_model
from django.db import models

PAYMENT_CHOICES = (
    ('PS', 'PayStack'),
)

User = get_user_model()

def get_sentinel_user():
    return User.objects.get_or_create(email='deleted_user@paymentapp.py')[0]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    order_id = models.PositiveBigIntegerField()
    reference = models.CharField(max_length=50, unique=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_CHOICES)
    amount = models.FloatField()
    verified = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user, self.reference)
