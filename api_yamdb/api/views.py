from secrets import token_urlsafe

from rest_framework import mixins, viewsets, status
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

User = get_user_model()


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Title.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering = ('year',)

    serializer_classes = {
        'list': TitleSerializerGet,
        'retrieve': TitleSerializerGet,
        'create': TitleSerializerPost,
        'update': TitleSerializerPost,
        'partial_update': TitleSerializerPost,
    }
    default_serializer_class = TitleSerializerGet

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,
                                           self.default_serializer_class)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = TitleSerializerGet(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(instance_serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        instance_serializer = TitleSerializerGet(instance)

        return Response(instance_serializer.data)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermissions]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_update(self, serializer):
        review = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, review)
        return serializer.save()

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
        user = User.objects.get(username=request.user.username)
        if request.method == 'PATCH':
            if 'role' in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def api_signup(request):
    user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email'))
    if user:
        serializer = SignupSerializer(
            user[0],
            data=request.data,
            partial=True)
    else:
        serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        code = token_urlsafe(20)
        serializer.save(confirmation_code=code)
        send_mail(
            subject='Ваш код аутентификации',
            message='Сохраните код! Он понадобится вам для получения токена.\n'
                    f'confirmation_code:\n{code}\n',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[serializer.data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(APIView):

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data["username"]
            confirmation_code = serializer.data["confirmation_code"]
            user = get_object_or_404(User, username=username)
            if user.confirmation_code != confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
