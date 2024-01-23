# Generated by Django 4.2.7 on 2024-01-07 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0023_alter_inventorytransfer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorytransfer',
            name='to_dc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_dc', to='crud_app.benchstock_part_in_dc'),
        ),
    ]
