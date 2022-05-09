# Generated by Django 2.1 on 2018-08-15 17:50

from django.db import migrations

from core.utils import get_unique_slug

GENRES = (
    {'code': 'adv_animal', 'description': 'Природа и животные', },
    {'code': 'adv_geo', 'description': 'Путешествия и география', },
    {'code': 'adv_history', 'description': 'Исторические приключения', },
    {'code': 'adv_indian', 'description': 'Приключения про индейцев', },
    {'code': 'adv_maritime', 'description': 'Морские приключения', },
    {'code': 'adv_western', 'description': 'Вестерн', },
    {'code': 'adventure', 'description': 'Прочие приключения', },
    {'code': 'antique', 'description': 'Прочая старинная литература', },
    {'code': 'antique_ant', 'description': 'Античная литература', },
    {'code': 'antique_east', 'description': 'Древневосточная литература', },
    {'code': 'antique_european', 'description': 'Европейская старинная литература', },
    {'code': 'antique_myths', 'description': 'Мифы. Легенды. Эпос', },
    {'code': 'antique_russian', 'description': 'Древнерусская литература', },
    {'code': 'child_adv', 'description': 'Детские приключения', },
    {'code': 'child_det', 'description': 'Детские остросюжетные', },
    {'code': 'child_education', 'description': 'Детская образовательная литература', },
    {'code': 'child_prose', 'description': 'Детскиая проза', },
    {'code': 'child_sf', 'description': 'Детская фантастика', },
    {'code': 'child_tale', 'description': 'Сказка', },
    {'code': 'child_verse', 'description': 'Детские стихи', },
    {'code': 'children', 'description': 'Прочая детская литература', },
    {'code': 'comp_db', 'description': 'Базы данных', },
    {'code': 'comp_hard', 'description': 'Компьютерное "железо"', },
    {'code': 'comp_osnet', 'description': 'ОС и Сети', },
    {'code': 'comp_programming', 'description': 'Программирование', },
    {'code': 'comp_soft', 'description': 'Программы', },
    {'code': 'comp_www', 'description': 'Интернет', },
    {'code': 'computers', 'description': 'Прочая околокомпьтерная литература', },
    {'code': 'design', 'description': 'Искусство и Дизайн', },
    {'code': 'det_action', 'description': 'Боевик', },
    {'code': 'det_classic', 'description': 'Классический детектив', },
    {'code': 'det_crime', 'description': 'Криминальный детектив', },
    {'code': 'det_espionage', 'description': 'Шпионский детектив', },
    {'code': 'det_hard', 'description': 'Крутой детектив', },
    {'code': 'det_history', 'description': 'Исторический детектив', },
    {'code': 'det_irony', 'description': 'Иронический детектив', },
    {'code': 'det_maniac', 'description': 'Маньяки', },
    {'code': 'det_police', 'description': 'Полицейский детектив', },
    {'code': 'det_political', 'description': 'Политический детектив', },
    {'code': 'detective', 'description': 'Детектив', },
    {'code': 'dramaturgy', 'description': 'Драматургия', },
    {'code': 'home', 'description': 'Прочиее домоводство', },
    {'code': 'home_cooking', 'description': 'Кулинария', },
    {'code': 'home_crafts', 'description': 'Хобби и ремесла', },
    {'code': 'home_diy', 'description': 'Сделай сам', },
    {'code': 'home_entertain', 'description': 'Развлечения', },
    {'code': 'home_garden', 'description': 'Сад и огород', },
    {'code': 'home_health', 'description': 'Здоровье', },
    {'code': 'home_pets', 'description': 'Домашние животные', },
    {'code': 'home_sex', 'description': 'Эротика, Секс', },
    {'code': 'home_sport', 'description': 'Спорт', },
    {'code': 'humor', 'description': 'Прочий юмор', },
    {'code': 'humor_anecdote', 'description': 'Анекдоты', },
    {'code': 'humor_prose', 'description': 'Юмористическая проза', },
    {'code': 'humor_verse', 'description': 'Юмористические стихи', },
    {'code': 'love_contemporary', 'description': 'Современные любовные романы', },
    {'code': 'love_detective', 'description': 'Остросюжетные любовные романы', },
    {'code': 'love_erotica', 'description': 'Эротика', },
    {'code': 'love_history', 'description': 'Исторические любовные романы', },
    {'code': 'love_short', 'description': 'Короткие любовные романы', },
    {'code': 'nonf_biography', 'description': 'Биографии и Мемуары', },
    {'code': 'nonf_criticism', 'description': 'Критика', },
    {'code': 'nonf_publicism', 'description': 'Публицистика', },
    {'code': 'nonfiction', 'description': 'Прочая документальная литература', },
    {'code': 'poetry', 'description': 'Поэзия', },
    {'code': 'prose_classic', 'description': 'Классическая проза', },
    {'code': 'prose_contemporary', 'description': 'Современная проза', },
    {'code': 'prose_counter', 'description': 'Контркультура', },
    {'code': 'prose_history', 'description': 'Историческая проза', },
    {'code': 'prose_rus_classic', 'description': 'Русская классическая проза', },
    {'code': 'prose_su_classics', 'description': 'Советская классическая проза', },
    {'code': 'ref_dict', 'description': 'Словари', },
    {'code': 'ref_encyc', 'description': 'Энциклопедии', },
    {'code': 'ref_guide', 'description': 'Руководства', },
    {'code': 'ref_ref', 'description': 'Справочники', },
    {'code': 'reference', 'description': 'Прочая справочная литература', },
    {'code': 'religion', 'description': 'Прочая религионая литература', },
    {'code': 'religion_esoterics', 'description': 'Эзотерика', },
    {'code': 'religion_rel', 'description': 'Религия', },
    {'code': 'religion_self', 'description': 'Самосовершенствование', },
    {'code': 'sci_biology', 'description': 'Биология', },
    {'code': 'sci_business', 'description': 'Деловая литература', },
    {'code': 'sci_chem', 'description': 'Химия', },
    {'code': 'sci_culture', 'description': 'Культурология', },
    {'code': 'sci_history', 'description': 'История', },
    {'code': 'sci_juris', 'description': 'Юриспруденция', },
    {'code': 'sci_linguistic', 'description': 'Языкознание', },
    {'code': 'sci_math', 'description': 'Математика', },
    {'code': 'sci_medicine', 'description': 'Медицина', },
    {'code': 'sci_philosophy', 'description': 'Философия', },
    {'code': 'sci_phys', 'description': 'Физика', },
    {'code': 'sci_politics', 'description': 'Политика', },
    {'code': 'sci_psychology', 'description': 'Психология', },
    {'code': 'sci_religion', 'description': 'Религиоведение', },
    {'code': 'sci_tech', 'description': 'Технические науки', },
    {'code': 'science', 'description': 'Прочая научная литература', },
    {'code': 'sf', 'description': 'Научная Фантастика', },
    {'code': 'sf_action', 'description': 'Боевая фантастика', },
    {'code': 'sf_cyberpunk', 'description': 'Киберпанк', },
    {'code': 'sf_detective', 'description': 'Детективная фантастика', },
    {'code': 'sf_epic', 'description': 'Эпическая фантастика', },
    {'code': 'sf_fantasy', 'description': 'Фэнтези', },
    {'code': 'sf_heroic', 'description': 'Героическая фантастика', },
    {'code': 'sf_history', 'description': 'Альтернативная история', },
    {'code': 'sf_horror', 'description': 'Ужасы и Мистика', },
    {'code': 'sf_humor', 'description': 'Юмористическая фантастика', },
    {'code': 'sf_social', 'description': 'Социально-психологическая фантастика', },
    {'code': 'sf_space', 'description': 'Космическая фантастика', },
    {'code': 'thriller', 'description': 'Триллер', },
)

def add_startup_data(apps, schema_editor):
    Genre = apps.get_model('library', 'Genre')
    for genre in GENRES:
        genre_object = Genre.objects.create(
            code=genre['code'],
            description=genre['description'],
        )
        genre_object.slug = get_unique_slug(
            genre_object,
            'slug',
            *('code', ),
            unique=True,
        )
        genre_object.save()

def remove_startup_data(apps, schema_editor):
    Genre = apps.get_model('library', 'genre')
    for genre in GENRES:
        genre_object = Genre.objects.get(code=genre['code'])
        genre_object.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_language_data'),
    ]

    operations = [
        migrations.RunPython(
            add_startup_data,
            remove_startup_data)
    ]