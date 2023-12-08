import django_filters
from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    GenreTitle,
    Comment)



# class TitleFilter(django_filters.FilterSet):
 
#     category = django_filters.ModelChoiceFilter(field_name="category__slug",
#                                             to_field_name='slug',
#                                             queryset=Category.objects.all())

#     class Meta:
#         model = Title
#         fields = ('category',)




class TitleFilter(django_filters.FilterSet):
 
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    
    class Meta():
       model = Title
       fields = ('category', 'genre', 'name', 'year')