from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()


class NameInfo(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class Genre(NameInfo):

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ["slug"]


class Category(NameInfo):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ["slug"]


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!')


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='title of the work')
    year = models.IntegerField(
        validators=[validate_year, ],
        verbose_name='release year')
    description = models.TextField(
        blank=True,
        null=True,
        default='',
        verbose_name='title of the work')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        blank=True,
        verbose_name='genre of the work')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='category of the work')

    class Meta:
        ordering = ["name"]
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name


class Review(models.Model):

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Оценка ниже 1!'
            ),
            MaxValueValidator(
                10,
                message='Оценка выше 10!'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'author',
                    'title'
                ],
                name='unique_author_title'
            ),
        )


class Comment(models.Model):

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
