# Generated by Django 4.2.1 on 2023-09-27 04:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_review_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coupon_code', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=250)),
                ('count', models.PositiveIntegerField(default=100)),
                ('discount_price', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=100)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
