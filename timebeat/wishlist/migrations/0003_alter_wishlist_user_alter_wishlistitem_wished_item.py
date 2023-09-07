# Generated by Django 4.2.3 on 2023-09-05 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', '0002_remove_wishlistitem_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='wished_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistitems', to='wishlist.wishlist'),
        ),
    ]
