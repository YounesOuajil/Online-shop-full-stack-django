# Generated by Django 4.2.1 on 2023-10-29 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chop', '0010_globalsalescount_shippingaddress_global_sales_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='global_sales_count',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='chop.globalsalescount'),
        ),
    ]
