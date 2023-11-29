from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre


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