from rest_framework import routers
from django.urls import include, path

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UsersViewSet,
    CustomAuthToken,
    api_signup)

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'users', UsersViewSet, basename='users')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

auth_urls = [
    path('signup/', api_signup, name='signup'),
    path('token/', CustomAuthToken.as_view(), name='token')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(v1_router.urls)),
]
