from django.contrib.auth import get_user_model
from django.db import DataError, models
from django.urls import reverse
from payments.models import Payment
from products.models import Product
from users.models import Address
from .managers import CartItemManager

User = get_user_model();

ORDER_STATUS = (
    ('UO', 'Not Ordered'),
    ('P', 'Processing'),
    ('BD', 'Being Delivered'),
    ('D', 'Delivered'),
    ('RR', 'Refund Requested'),
    ('RG', 'Refund Granted')
)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = CartItemManager()

    class Meta:
        verbose_name_plural = 'Cart Items'

    def save(self, *args, **kwargs):
        if self.product.is_active == False:
            raise DataError("Cannot add an Inactive Product to Cart")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}    of    {self.product}   by    {self.user}"

    def get_absolute_url(self):
        return reverse('cartitem', kwargs={'pk': self.pk})

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        if self.product.discount_price:
            return self.quantity * self.product.discount_price
        return 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(CartItem)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=2, default='UO', choices=ORDER_STATUS)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.user

    def get_total(self):
        total = CartItem.objects.get_final_price(self.user)
        return total
