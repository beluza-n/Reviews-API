from django.db import models


class Review(models.Model):
    pass


class Comment(models.Model):
    pass



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
    rating = models.ForeignKey(
        Review, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True)

    def __str__(self):
        return self.name
  

