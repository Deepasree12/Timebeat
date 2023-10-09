# Generated by Django 4.2.3 on 2023-10-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_remove_order_total_actual_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='total_price',
            new_name='total_actual_price',
        ),
        migrations.AddField(
            model_name='order',
            name='total_actual_price',
            field=models.IntegerField(default=0),
        ),
    ]
