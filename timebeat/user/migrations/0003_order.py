# Generated by Django 4.2.3 on 2023-09-12 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_mode', models.CharField(max_length=250)),
                ('payment_id', models.CharField(max_length=250, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Out For Shipping', 'Out For Shipping'), ('Completed', 'Completed')], default='pending', max_length=150)),
                ('message', models.TextField(null=True)),
                ('tracking_no', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='user.useraddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
