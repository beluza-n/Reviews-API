from rest_framework import serializers
from django.db.models import Avg
import datetime as dt

from reviews.models import Title, Category, Genre, Review, GenreTitle, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        qs = obj.reviews.all().aggregate(rating=Avg('score'))
        if qs['rating'] is not None:
            return round(list(qs.values())[0])
        else:
            return None


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.ListSerializer(child=serializers.CharField())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title
        optional_fields = ['description', ]

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = super().create(validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    def update(self, instance, validated_data):
        genres = validated_data.pop('genre')
        title = super().update(instance, validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre)
            GenreTitle.objects.filter(title=title).delete()
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return value

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('author', 'pub_date')
