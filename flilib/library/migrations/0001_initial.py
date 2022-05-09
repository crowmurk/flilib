# Generated by Django 4.0.3 on 2022-04-28 11:40

import core.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inpx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=128, verbose_name='Firstname')),
                ('middlename', models.CharField(blank=True, max_length=128, verbose_name='Middlename')),
                ('lastname', models.CharField(blank=True, max_length=128, verbose_name='Lastname')),
                ('slug', models.SlugField(allow_unicode=True, editable=False, help_text='A label for URL config.', max_length=512, unique=True, validators=[core.validators.validate_slug, django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), 'Enter a valid “slug” consisting of Unicode letters, numbers, underscores, or hyphens.', 'invalid')])),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ('lastname', 'firstname', 'middlename'),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, verbose_name='Title')),
                ('seriesnumber', models.IntegerField(blank=True, null=True, verbose_name='Series number')),
                ('file', models.CharField(max_length=256, verbose_name='File')),
                ('size', models.PositiveIntegerField(verbose_name='Size')),
                ('libraryid', models.PositiveIntegerField(unique=True, verbose_name='Library ID')),
                ('deleted', models.BooleanField(verbose_name='Deleted')),
                ('extension', models.CharField(blank=True, max_length=8, verbose_name='Extension')),
                ('date', models.DateField(verbose_name='Date')),
                ('libraryrate', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Library rate')),
                ('keywords', models.CharField(blank=True, max_length=512, verbose_name='Keywords')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True, verbose_name='Code')),
                ('description', models.CharField(blank=True, max_length=128, verbose_name='Description')),
                ('slug', models.SlugField(editable=False, help_text='A label for URL config.', max_length=64, unique=True, validators=[core.validators.validate_slug])),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'ordering': ('description',),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True, verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=64, verbose_name='Name')),
                ('slug', models.SlugField(editable=False, help_text='A label for URL config.', max_length=2, unique=True, validators=[core.validators.validate_slug])),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(allow_unicode=True, editable=False, help_text='A label for URL config.', max_length=256, unique=True, validators=[core.validators.validate_slug, django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), 'Enter a valid “slug” consisting of Unicode letters, numbers, underscores, or hyphens.', 'invalid')])),
            ],
            options={
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='series',
            constraint=models.CheckConstraint(check=models.Q(('name__gt', '')), name='library_series.name_required'),
        ),
        migrations.AddField(
            model_name='bookgenre',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book'),
        ),
        migrations.AddField(
            model_name='bookgenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.genre'),
        ),
        migrations.AddField(
            model_name='bookauthor',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.author'),
        ),
        migrations.AddField(
            model_name='bookauthor',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book'),
        ),
        migrations.AddField(
            model_name='book',
            name='archive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='inpx.inp', verbose_name='Archive'),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='books', through='library.BookAuthor', to='library.author', verbose_name='Authors'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='books', through='library.BookGenre', to='library.genre', verbose_name='Genres'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books', to='library.language', verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books', to='library.series', verbose_name='Series'),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('lastname__gt', ''), ('firstname__gt', ''), ('middlename__gt', ''), _connector='OR'), name='library_author_all_names_are_blank'),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('lastname', 'firstname', 'middlename')},
        ),
        migrations.AlterUniqueTogether(
            name='bookgenre',
            unique_together={('book', 'genre')},
        ),
        migrations.AlterUniqueTogether(
            name='bookauthor',
            unique_together={('book', 'author')},
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('series__isnull', True), ('seriesnumber__isnull', True)), ('series__isnull', False), _connector='OR'), name='library_book.seriesnumber_without_series'),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.CheckConstraint(check=models.Q(('file__gt', '')), name='library_book.file_required'),
        ),
    ]