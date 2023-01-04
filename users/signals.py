from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Address


@receiver(post_save, sender=Address)
def check_default_address(sender, instance, created, **kwargs):
    if created and instance.default == True:
        addresses = Address.objects.filter(
            user=instance.user, address_type=instance.address_type, default=True
        ).exclude(id=instance.id)
        if addresses.exists():
            for address in addresses:
                address.default = False
                address.save()
