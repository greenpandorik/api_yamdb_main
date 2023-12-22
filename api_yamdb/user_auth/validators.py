import re

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from users.models import User


def validate_username(value):
    if value == 'me' or not re.match(settings.REGEX, value):
        raise ValidationError('Недопустимое имя пользователя!')


def correct_fields(data):

    username_exist = User.objects.filter(
        username=data['username']
    ).exists()

    email_exist = User.objects.filter(
        email=data['email'],
    ).exists()

    if username_exist:
        user = get_object_or_404(User, username=data['username'])
        if email_exist and user.email != data['email']:
            raise ValidationError('Ошибка в веденных данных')
        if not email_exist and user.email != data['email']:
            raise ValidationError('email введен некорректно')

    if email_exist:
        user = get_object_or_404(User, email=data['email'])
        if not username_exist and user.username != data['username']:
            raise ValidationError('username введен некорректно')
    return data


def check_token(data):
    user = get_object_or_404(User, username=data['username'])
    confirmation_code = data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        raise ValidationError('Неверный код подтверждения')
    return data
