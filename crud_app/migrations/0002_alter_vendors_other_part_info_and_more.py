# Generated by Django 4.2.7 on 2023-12-18 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors',
            name='other_part_info',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='other_vendor_info',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]