# Generated by Django 4.1 on 2023-09-28 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='coordinates',
        ),
        migrations.DeleteModel(
            name='Coordinate',
        ),
    ]
