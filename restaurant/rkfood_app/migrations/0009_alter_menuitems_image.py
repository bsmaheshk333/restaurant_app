# Generated by Django 5.1 on 2024-09-02 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rkfood_app', '0008_menuitems_image_alter_menuitems_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitems',
            name='image',
            field=models.ImageField(default='avatar.jpg', upload_to='menu_items/', verbose_name='image of the food'),
        ),
    ]