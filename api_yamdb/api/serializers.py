from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = Category

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = Genre


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
