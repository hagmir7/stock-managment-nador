# Generated by Django 4.1.3 on 2022-12-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0014_payment_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]