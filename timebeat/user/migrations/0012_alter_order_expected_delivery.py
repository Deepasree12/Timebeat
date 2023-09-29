# Generated by Django 4.2.3 on 2023-09-19 06:26

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_order_expected_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expected_delivery',
            field=models.DateTimeField(default=django.db.models.expressions.CombinedExpression(models.F('created_at'), '+', models.Value(datetime.timedelta(days=3)))),
        ),
    ]