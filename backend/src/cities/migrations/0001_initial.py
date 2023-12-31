# Generated by Django 4.1 on 2023-09-18 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('population', models.PositiveIntegerField(verbose_name='Население')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=32, verbose_name='Широта')),
                ('longitude', models.CharField(max_length=32, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Координата',
                'verbose_name_plural': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, unique=True, verbose_name='Часовой пояс')),
                ('utc', models.CharField(max_length=4, unique=True, verbose_name='UTC')),
            ],
            options={
                'verbose_name': 'Временная зона',
                'verbose_name_plural': 'Временные зоны',
            },
        ),
        migrations.AddConstraint(
            model_name='coordinate',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude'), name='Проверка уникальности координат'),
        ),
        migrations.AddField(
            model_name='city',
            name='coordinates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city', to='cities.coordinate', verbose_name='Координаты'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='countries.state', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='city',
            name='time_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city', to='cities.timezone', verbose_name='Часовой пояс'),
        ),
    ]
