# Generated by Django 4.0.3 on 2022-04-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenreAlias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True, verbose_name='Code')),
            ],
        ),
        migrations.CreateModel(
            name='Inp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=256, unique=True, verbose_name='File')),
                ('mdhash', models.CharField(max_length=32, unique=True, verbose_name='Hash')),
            ],
        ),
        migrations.CreateModel(
            name='LanguageAlias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, unique=True, verbose_name='Code')),
            ],
        ),
    ]
