# Generated by Django 3.2.5 on 2021-07-07 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_payment_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='transaction_id',
            new_name='reference',
        ),
    ]
