# Generated by Django 4.2.1 on 2023-10-29 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chop', '0008_rename_zipcode_shippingaddress_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
    ]
