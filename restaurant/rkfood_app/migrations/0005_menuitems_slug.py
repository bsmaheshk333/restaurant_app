# Generated by Django 5.1 on 2024-09-27 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rkfood_app', '0004_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitems',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]
