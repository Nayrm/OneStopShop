# Generated by Django 4.2.7 on 2023-12-19 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0003_alter_furniture_furniture_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchstock_part',
            name='benchstock_sku',
            field=models.PositiveIntegerField(editable=False, unique=True),
        ),
    ]
