# Generated by Django 4.2.3 on 2023-09-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_order_expected_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
