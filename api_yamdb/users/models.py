from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    (settings.USER, 'Пользователь'),
    (settings.MODERATOR, 'Модератор'),
    (settings.ADMIN, 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Права доступа',
        max_length=16,
        choices=ROLES,
        default='user'
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        ordering = ['-id']

    @property
    def is_user(self):
        return self.role == settings.USER

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == settings.ADMIN
            or self.is_staff
        )
