from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator)

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug



class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    # rating = models.ForeignKey(
    #     Review, on_delete=models.SET_NULL,
    #     related_name='titles', blank=True, null=True)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True)

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
        on_delete=models.CASCADE
    )


    class Meta:
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
