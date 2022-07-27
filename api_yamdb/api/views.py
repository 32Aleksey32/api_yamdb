from rest_framework import filters, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .pagination import UsersPagination

from reviews.models import Title, Category, Genre, User
from .permissions import IsAdmin
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer,
                          UsersSerializer, SignupSerializer, MeSerializer,
                          JwtTokenSerializer)

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
