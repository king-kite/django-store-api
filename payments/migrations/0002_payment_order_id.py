# Generated by Django 3.2.5 on 2021-07-06 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_id',
            field=models.PositiveBigIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
