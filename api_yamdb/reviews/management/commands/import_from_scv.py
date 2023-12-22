import os

from django.core.management.base import BaseCommand, CommandError


DICT = {
    'users_user': 'users.csv',
    'reviews_genre': 'genre.csv',
    'reviews_category': 'category.csv',
    'reviews_title': 'titles.csv',
    'reviews_review': 'review.csv',
    'reviews_comment': 'comments.csv',
    'reviews_title_genre': 'genre_title.csv'
}


class Command(BaseCommand):
    help = u'Импортируем данные из файлов CSV в BD'

    def handle(self, *args, **kwargs):
        try:
            for bd, file in DICT.items():
                os.system(
                    f'sqlite3 ./db.sqlite3 ".mode csv"  ".import'
                    f' static/data/{file} {bd}"')
        except Exception as error:
            CommandError(error)
