# Generated by Django 3.2.5 on 2021-07-04 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210704_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Processing'), ('BD', 'Being Delivered'), ('D', 'Delivered'), ('RR', 'Refund Requested'), ('RG', 'Refund Granted')], default='P', max_length=2),
        ),
    ]
