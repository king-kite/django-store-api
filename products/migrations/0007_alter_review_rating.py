# Generated by Django 3.2.5 on 2021-07-03 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='5', max_length=1),
        ),
    ]