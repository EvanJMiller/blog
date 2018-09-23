# Generated by Django 2.0.1 on 2018-09-20 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20180920_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='header',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='portrait',
            field=models.ImageField(default='default.png', upload_to='media/'),
        ),
    ]
