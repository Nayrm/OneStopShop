# Generated by Django 4.2.7 on 2023-12-31 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0017_slatinformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slatinformation',
            name='center_slat_amount',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='center_slat_length',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='mid_support_amount',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='mid_support_height',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='slat_amount',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='slat_length',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='support_amount',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='slatinformation',
            name='support_height',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
