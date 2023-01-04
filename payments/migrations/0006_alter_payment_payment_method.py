# Generated by Django 3.2.5 on 2021-07-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_rename_transaction_id_payment_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('PS', 'PayStack'), ('R', 'Remita')], max_length=3),
        ),
    ]