from rest_framework import filters, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .pagination import UsersPagination

from reviews.models import Title, Category, Genre, User
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer,
                          UsersSerializer, SignupSerializer, JwtTokenSerializer,
                          MeSerializer)

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUser,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UsersSerializer
    pagination_class = UsersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
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
        return Response(serializer.errors)


class SignupView(views.APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email').lower()
        username = serializer.validated_data.get('username')
        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(
                email=email, username=username)
        else:
            if User.objects.filter(username=username).exists():
                return Response(f'Пользователь с username = {username}'
                                ' уже существует',
                                status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response(f'Пользователь с email = {email} уже существует',
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Код подтверждения'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(mail_subject,
                  message,
                  settings.EMAIL_FROM,
                  [email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(views.APIView):

    def post(self, request):
        serializer = JwtTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=self.request.data.get('username'))
        if serializer.data['confirmation_code'] == str(
            user.confirmation_code
        ) and user.is_active:
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
