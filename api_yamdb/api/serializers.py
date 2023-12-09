import re
import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)


User = get_user_model()


class ValidateUsernameMixin(object):
    def validate_username(self, value):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if not pattern.match(value) or value == 'me' or len(value) > 150:
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!')
        return value


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
    description = serializers.SerializerMethodField()

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

    def get_description(self, instance):
        if instance.description is None:
            return ''
        return instance.description


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title
        optional_fields = ['description', ]

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = super().create(validated_data)
        title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        if 'genre' not in self.initial_data:
            title = super().update(instance, validated_data)
            return title

        genres = validated_data.pop('genre')
        title = super().update(instance, validated_data)
        for genre in genres:
            GenreTitle.objects.filter(title=title).delete()
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return value

    def validate_genre(self, value):
        clear_genre = []
        for genre in value:
            try:
                current_genre = Genre.objects.get(slug=genre)
            except Genre.DoesNotExist:
                raise serializers.ValidationError(
                    'Такого жанра нет')
            clear_genre.append(current_genre)
        return clear_genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=author, title=title_id).exists():
                raise ValidationError('К произведению нельзя добавлять более '
                                      'одного комментария!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class SignupSerializer(
    ValidateUsernameMixin,
    serializers.ModelSerializer
):

    class Meta:
        fields = ('username', 'email',)
        extra_kwargs = {
            'confirmation_code': {
                'write_only': True
            }
        }
        model = User


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=27)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role

        return token


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
