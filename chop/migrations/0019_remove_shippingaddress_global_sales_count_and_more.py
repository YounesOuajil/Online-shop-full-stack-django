# Generated by Django 4.2.1 on 2023-10-29 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chop', '0018_remove_order_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='global_sales_count',
        ),
        migrations.DeleteModel(
            name='GlobalSalesCount',
        ),
    ]