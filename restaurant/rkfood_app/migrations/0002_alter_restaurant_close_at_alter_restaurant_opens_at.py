# Generated by Django 5.1 on 2024-09-12 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rkfood_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='close_at',
            field=models.TimeField(verbose_name='close time'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='opens_at',
            field=models.TimeField(verbose_name='opening time'),
        ),
    ]