# Generated by Django 4.2.7 on 2023-12-31 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0016_alter_vendors_sends_parts'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlatInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.PositiveIntegerField(unique=True)),
                ('slat_amount', models.PositiveIntegerField(max_length=3)),
                ('slat_length', models.PositiveIntegerField(max_length=3)),
                ('center_slat_amount', models.PositiveIntegerField(max_length=3)),
                ('center_slat_length', models.PositiveIntegerField(max_length=3)),
                ('support_amount', models.PositiveIntegerField(max_length=3)),
                ('support_height', models.PositiveIntegerField(max_length=3)),
                ('mid_support_amount', models.PositiveIntegerField(max_length=3)),
                ('mid_support_height', models.PositiveIntegerField(max_length=3)),
                ('notes', models.TextField(blank=True, max_length=500)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crud_app.vendors')),
            ],
        ),
    ]