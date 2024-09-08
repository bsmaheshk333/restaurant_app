# Generated by Django 5.1 on 2024-09-02 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rkfood_app', '0007_alter_order_customer_alter_order_menu_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitems',
            name='image',
            field=models.ImageField(default='avatar.jpg', upload_to='images/', verbose_name='image of the food'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_menu', to='rkfood_app.menu'),
        ),
    ]
