from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import CartItem, Order


def get_order(user):
    try:
        order = Order.objects.get(user=user, ordered=False)
        return order
    except Order.DoesNotExist:
        return None

@receiver(post_save, sender=CartItem)
def get_or_create_order(sender, instance, created,  **kwargs):
    if created and instance.ordered is False:
        order = get_order(instance.user)
        if order:
            order.products.add(instance)
        else:
            order = Order.objects.create(user=instance.user)
            order.products.set([instance])

@receiver(post_delete, sender=CartItem)
def delete_order_if_no_cart_item_available(sender, instance, **kwargs):
    order = get_order(instance.user)
    if order and order.products.count() == 0:
        order.delete()

@receiver(post_save, sender=Order)
def set_cart_items_order_status(sender, instance, **kwargs):
    if instance.ordered == True:
        for item in instance.products.all():
            item.ordered = True
            item.save()
    else:
        for item in instance.products.all():
            item.ordered = False
            item.save()
