from rest_framework import routers
from django.urls import include, path
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
