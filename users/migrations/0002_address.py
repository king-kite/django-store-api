# Generated by Django 3.2.5 on 2021-07-04 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=100, verbose_name='Street Address')),
                ('address2', models.CharField(max_length=100, verbose_name='Apartment/Suite/House No.')),
                ('country', django_countries.fields.CountryField(default='NG', max_length=2)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=50)),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
