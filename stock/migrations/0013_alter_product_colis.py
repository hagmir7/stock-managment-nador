# Generated by Django 4.1.3 on 2022-12-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colis',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
