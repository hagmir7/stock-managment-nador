# Generated by Django 4.1.3 on 2022-12-05 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_order_total_orderitem_alter_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='product_order', to='stock.orderitem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
