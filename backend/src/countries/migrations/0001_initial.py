# Generated by Django 4.1 on 2023-09-18 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Континент',
                'verbose_name_plural': 'Континенты',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('full_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Полное название')),
                ('capital', models.CharField(blank=True, max_length=256, null=True, verbose_name='Столица')),
                ('population', models.PositiveIntegerField(verbose_name='Население')),
                ('size', models.PositiveBigIntegerField(verbose_name='Размер')),
                ('code', models.CharField(max_length=2, unique=True, verbose_name='Код')),
                ('phone_code', models.CharField(max_length=4, verbose_name='Телефонный код')),
                ('continent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='countries.continent', verbose_name='Континент')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country', to='currencies.currency', verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Язык',
                'verbose_name_plural': 'Языки',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('code', models.CharField(max_length=2, verbose_name='Код')),
                ('num_cities', models.PositiveIntegerField(verbose_name='Количество городов')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='countries.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Область',
                'verbose_name_plural': 'Области',
            },
        ),
        migrations.AddField(
            model_name='country',
            name='languages',
            field=models.ManyToManyField(related_name='countries', to='countries.language'),
        ),
    ]
