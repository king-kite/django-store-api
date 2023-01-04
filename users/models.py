from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_countries.fields import CountryField
from .managers import AddressManager, UserManager

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    is_active = models.BooleanField(default=True, help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
            ))
    is_admin = models.BooleanField(default=False, help_text=(
            'Designates whether this user is a staff and can log into the admin site. '
            ))
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    address1 = models.CharField(max_length=100, verbose_name='Street Address')
    address2 = models.CharField(max_length=100, verbose_name='Apartment/Suite/House No.')
    country = CountryField(multiple=False, default='NG')
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=50)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, default='S')
    default = models.BooleanField(default=False)

    objects = AddressManager()

    class Meta:
        verbose_name_plural= "Addresses"

    def __str__(self):
        return '%s %s' % (self.user, self.address_type)
