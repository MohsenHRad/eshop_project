# Generated by Django 5.0.1 on 2024-09-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0007_remove_product_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_count',
            field=models.IntegerField(default=0, verbose_name='تعداد محصول'),
        ),
    ]
