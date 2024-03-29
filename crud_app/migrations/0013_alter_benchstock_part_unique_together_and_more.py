# Generated by Django 4.2.7 on 2023-12-23 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0012_rename_self_side_benchstock_part_in_dc_shelf_side'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='benchstock_part',
            unique_together={('vendor', 'part_type', 'part_description', 'part_color')},
        ),
        migrations.AlterUniqueTogether(
            name='benchstock_part_in_dc',
            unique_together={('dc', 'benchstock_part')},
        ),
    ]
