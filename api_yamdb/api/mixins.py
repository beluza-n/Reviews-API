import re

from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .permissions import IsAdminUserOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class NameViewSetMixin(ListCreateDestroyViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class ValidateUsernameMixin(object):
    def validate_username(self, value):
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if not pattern.match(value) or value == 'me' or len(value) > 150:
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!')
        return value
