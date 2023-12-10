from secrets import token_urlsafe
from django.db.models import Avg
from django.db.models import IntegerField
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Category, Genre, Review
from .permissions import (
    IsAdmin,
    IsAdminUserOrReadOnly,
    ReviewCommentPermissions
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import (
    CategorySerializer,
    TitleSerializerGet,
    TitleSerializerPost,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    SignupSerializer,
    AuthSerializer,
)
from .filters import TitleFilter
from .mixins import NameViewSetMixin

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = (Title.objects.annotate(
        rating=Avg('reviews__score', output_field=IntegerField()))
        .order_by('year'))
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering = ('year',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleSerializerPost
        return TitleSerializerGet


class CategoryViewSet(NameViewSetMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(NameViewSetMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermissions]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermissions]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (SearchFilter,)
    http_method_names = ['get', 'post', 'delete', 'patch']
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me',
        url_name='me')
    def my_user(self, request):
        user = request.user
        if request.method == 'PATCH':
            if 'role' in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def api_signup(request):
    user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).first()
    if user:
        serializer = SignupSerializer(
            user,
            data=request.data,
            partial=True)
    else:
        serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = token_urlsafe(20)
    serializer.save(confirmation_code=code)
    send_mail(
        subject='Ваш код аутентификации',
        message='Сохраните код! Он понадобится вам для получения токена.\n'
                f'confirmation_code:\n{code}\n',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[serializer.validated_data['email']],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(APIView):

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        confirmation_code = serializer.validated_data["confirmation_code"]
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
