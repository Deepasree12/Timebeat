# Generated by Django 4.2.3 on 2023-10-05 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_alter_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='total_actual_price',
        ),
    ]
