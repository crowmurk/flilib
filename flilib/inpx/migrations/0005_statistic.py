# Generated by Django 4.0.3 on 2022-05-06 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inpx', '0004_genre_alias_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors_database', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Authors in database')),
                ('authors_library', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Authors in library')),
                ('genres_database', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Genres in database')),
                ('genres_library', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Genres in library')),
                ('languages_database', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Languages in database')),
                ('languages_library', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Languages in library')),
                ('series_database', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Series in database')),
                ('series_library', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Series in library')),
                ('books_database', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Books in database')),
                ('books_library', models.PositiveIntegerField(blank=True, editable=False, verbose_name='Books in library')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Update date')),
                ('time_spent', models.DurationField(blank=True, editable=False, verbose_name='Update time spent')),
            ],
            options={
                'verbose_name': 'Database statistic',
                'verbose_name_plural': 'Database statistic',
                'ordering': ('date',),
            },
        ),
    ]
