# Generated by Django 4.2.3 on 2023-08-24 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_rename_total_discount_cartitem_total_discount_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='total_discount_price',
            new_name='discount_price',
        ),
    ]
