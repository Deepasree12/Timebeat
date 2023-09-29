# Generated by Django 4.2.3 on 2023-09-23 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_variant_created_at'),
        ('user', '0017_alter_order_status_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='Product_variant',
        ),
        migrations.AddField(
            model_name='review',
            name='Product',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product'),
        ),
    ]