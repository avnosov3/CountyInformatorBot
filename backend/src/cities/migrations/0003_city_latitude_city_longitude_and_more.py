# Generated by Django 4.1 on 2023-09-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_remove_city_coordinates_delete_coordinate'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.CharField(default='1', max_length=32, verbose_name='Широта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.CharField(default='0', max_length=32, verbose_name='Долгота'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude'), name='Проверка уникальности координат'),
        ),
    ]
