from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .validators import validate_year

User = get_user_model()


class NameInfo(models.Model):
    name = models.CharField(max_length=256, verbose_name='abstract name')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='abstract slug'
    )

    class Meta:
        abstract = True
        verbose_name = 'nameInfo'
        verbose_name_plural = 'nameInfo'

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

    text = models.TextField(verbose_name='text of the review')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author of the review'
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
        ],
        verbose_name='score of the review'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='publication date'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title described in review'
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

    text = models.TextField(verbose_name='text of the comment')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author of the review'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='publication date'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review described in comment'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
