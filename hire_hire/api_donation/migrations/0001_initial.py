# Generated by Django 4.2a1 on 2023-07-06 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        choices=[('RUB', 'Рубли')],
                        max_length=10,
                        verbose_name='наименование',
                    ),
                ),
            ],
            options={
                'verbose_name': 'валюта',
                'verbose_name_plural': 'валюты',
            },
        ),
        migrations.CreateModel(
            name='IdempotenceKey',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('value', models.UUIDField(verbose_name='значение')),
                (
                    'creation_date',
                    models.DateField(
                        auto_now_add=True, verbose_name='дата создания'
                    ),
                ),
            ],
            options={
                'verbose_name': 'ключ идемпотенции',
                'verbose_name_plural': 'ключи идемпотенции',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('value', models.IntegerField(verbose_name='значение')),
                (
                    'currency',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='api_donation.currency',
                        verbose_name='валюта',
                    ),
                ),
            ],
            options={
                'verbose_name': 'цена',
                'verbose_name_plural': 'цены',
            },
        ),
    ]
