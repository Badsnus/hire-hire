# Generated by Django 4.2a1 on 2023-03-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('interview', '0008_category_language_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(
                default='python3_logo.jpg',
                help_text='иконка',
                upload_to='icons',
                verbose_name='иконка',
            ),
        ),
        migrations.AddField(
            model_name='language',
            name='icon',
            field=models.ImageField(
                default='python3_logo.jpg',
                help_text='иконка',
                upload_to='icons',
                verbose_name='иконка',
            ),
        ),
    ]
