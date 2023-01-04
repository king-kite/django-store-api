from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.db import models
from django.urls import reverse

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    )

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_reviews_url(self):
        return reverse('reviews', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='products/images/')
    main = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name='user_reviews', default='Anonymous')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_reviews', blank=True, null=True)
    body = models.TextField()
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default='5')
    is_approved = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['author', 'product']

    def __str__(self):
        return '%s %s' % (self.author, self.product)

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.body or self.body == '':
            raise ValueError("Review body cannot be an empty field!")
        if self.product.is_active == False:
            raise FieldError("This Product Is no longer valid!")
        super().save(*args, **kwargs)
