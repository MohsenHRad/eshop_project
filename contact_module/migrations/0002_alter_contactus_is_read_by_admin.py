# Generated by Django 5.0.1 on 2024-03-13 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='is_read_by_admin',
            field=models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین'),
        ),
    ]
