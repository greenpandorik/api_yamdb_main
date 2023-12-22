from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Дата выпуска', validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому будет относиться отзыв'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[
        MinValueValidator(
            1,
            message='Оценка должна быть больше единицы'
        ),
        MaxValueValidator(
            10,
            message='Оценка должна быть меньше десяти'
        ),
    ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique follow')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому будет относиться комментарий'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text
