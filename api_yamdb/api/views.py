from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from reviews.models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


from rest_framework.pagination import PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = PageNumberPagination

class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass