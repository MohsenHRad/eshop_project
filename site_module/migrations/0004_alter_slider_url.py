# Generated by Django 5.0.1 on 2024-07-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_slider_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='url',
            field=models.URLField(max_length=500, verbose_name='آدرس لینک'),
        ),
    ]
