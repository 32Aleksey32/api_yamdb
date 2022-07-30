from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.mixins import (DestroyModelMixin, CreateModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import (IsAuthenticated, AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Category, Genre, User, Review
from .filter import TitleFilter
from .pagination import (UsersPagination, CategoriesPagination,
                         GenresPagination, TitlesPagination,
                         ReviewsPagination, CommentsPagination)
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdmin
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer,
                          UsersSerializer, SignupSerializer, MeSerializer,
                          JwtTokenSerializer, ReviewSerializer,
                          CommentSerializer, TitleReadSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = TitlesPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = CategoriesPagination
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = GenresPagination
    lookup_field = 'slug'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UsersSerializer
    pagination_class = UsersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = MeSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MeSerializer(
            self.request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error_messages)


class SignupView(views.APIView):

    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email').lower()
        username = serializer.validated_data.get('username')
        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(
                email=email, username=username)
        else:
            if User.objects.filter(username=username).exists():
                return Response(serializer.error_messages,
                                status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response(serializer.error_messages,
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Confirmation code'
        message = f'Your confirmation code: {confirmation_code}'
        send_mail(mail_subject,
                  message,
                  settings.EMAIL_FROM,
                  [email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(views.APIView):

    serializer_class = JwtTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data.get('username'))
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(
            serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = ReviewsPagination

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            return (IsAuthorOrAdmin(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CommentsPagination

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            return (IsAuthorOrAdmin(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(
            review=review,
            author=self.request.user
        )
