# Generated by Django 3.1.1 on 2020-09-07 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to='profile_pics'),
        ),
    ]