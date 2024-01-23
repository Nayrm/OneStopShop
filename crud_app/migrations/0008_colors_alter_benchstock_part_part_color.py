# Generated by Django 4.2.7 on 2023-12-20 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud_app', '0007_delete_userdc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_options', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='benchstock_part',
            name='part_color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crud_app.colors'),
        ),
    ]
