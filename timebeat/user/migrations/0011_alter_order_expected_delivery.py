# Generated by Django 4.2.3 on 2023-09-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_order_tracking_no_order_expected_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expected_delivery',
            field=models.DateTimeField(),
        ),
    ]
