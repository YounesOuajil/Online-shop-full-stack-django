# Generated by Django 4.2.1 on 2023-10-09 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='USER',
            new_name='client',
        ),
    ]
