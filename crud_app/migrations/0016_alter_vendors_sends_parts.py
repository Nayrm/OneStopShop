# Generated by Django 4.2.7 on 2023-12-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0015_remove_vendors_other_vendor_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors',
            name='sends_parts',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3),
        ),
    ]
