# Generated by Django 4.2.3 on 2023-10-17 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_alter_order_expected_delivery_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expected_delivery',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 10, 20, 6, 55, 1, 77981, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
