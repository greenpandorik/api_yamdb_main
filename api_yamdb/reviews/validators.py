from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now_year = timezone.now().year
    if value > now_year:
        raise ValidationError(
            f'{value} Год выпуска не может быть '
            f'больше текущего года {now_year}'
        )
