# Generated by Django 5.0.1 on 2024-07-14 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('url', models.CharField(max_length=200, verbose_name='آدرس لینک')),
                ('url_title', models.CharField(max_length=200, verbose_name='عنوان لینک')),
                ('description', models.TextField(max_length=700, verbose_name='توضیحات')),
                ('image', models.ImageField(upload_to='images/slider', verbose_name='تصویر اسلایدر')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدر ها',
            },
        ),
    ]
