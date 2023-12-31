# Generated by Django 4.2.3 on 2023-09-12 00:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_variant_product'),
        ('user', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.order')),
            ],
        ),
    ]
