# Generated by Django 4.0.3 on 2022-05-06 08:16

from django.db import migrations
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_genre_data'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='author',
            managers=[
                ('objects', library.models.AuthorManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='genre',
            managers=[
                ('objects', library.models.GenreManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='language',
            managers=[
                ('objects', library.models.LanguageManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='series',
            managers=[
                ('objects', library.models.SeriesManager()),
            ],
        ),
    ]
