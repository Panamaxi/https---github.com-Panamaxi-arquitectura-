# Generated by Django 5.0.6 on 2024-10-17 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZonaGamers', '0007_juego_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='juego',
            name='codigo',
        ),
        migrations.AddField(
            model_name='juego',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
