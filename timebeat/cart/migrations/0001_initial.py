# Generated by Django 4.2.3 on 2023-08-22 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('total_selling_price', models.IntegerField(default=0)),
                ('total_actual_price', models.IntegerField(default=0)),
                ('cart', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='cart.cart')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='store.variant')),
            ],
        ),
    ]
