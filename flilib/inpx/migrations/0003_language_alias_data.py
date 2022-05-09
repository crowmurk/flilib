# Generated by Django 2.1 on 2018-08-15 17:50

from django.db import migrations

ALIASES = {
    'EN-US': 'en',
    'RU': 'ru',
    'ru~': 'ru',
    'ru-': 'ru',
    'sah': '',
    'sp': 'es',
    'ua': 'uk',
    'un': '',
    'und': '',
    'xx': '',
    'кг': 'ru',
}

def add_startup_data(apps, schema_editor):
    Language = apps.get_model('library', 'Language')
    LanguageAlias = apps.get_model('inpx', 'LanguageAlias')
    for code, language in ALIASES.items():
        if language:
            LanguageAlias.objects.create(
                code=code,
                language=Language.objects.get(code=language),
            )

def remove_startup_data(apps, schema_editor):
    LanguageAlias = apps.get_model('inpx', 'LanguageAlias')
    for code, language in ALIASES.items():
        if language:
            language_alias_object = LanguageAlias.objects.get(code=code)
            language_alias_object.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inpx', '0002_initial'),
        ('library', '0002_language_data'),
    ]

    operations = [
        migrations.RunPython(
            add_startup_data,
            remove_startup_data)
    ]