# Generated by Django 5.0.1 on 2024-07-21 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0003_user_about_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about_author',
            field=models.TextField(blank=True, null=True, verbose_name='درباره شخص'),
        ),
    ]
