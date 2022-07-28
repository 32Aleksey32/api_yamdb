from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import RegexValidator
from reviews.models import Title, Category, Genre, User
from rest_framework.relations import SlugRelatedField
import datetime as dt


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')
    genre = SlugRelatedField(slug_field='slug', read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value < year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя задано некорректно',
        ),
    ])
#    validators = [
#            UniqueTogetherValidator(
#                queryset=User.objects.all(),
#                fields=('email', 'username')
#            )
#        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве username запрещено.')
        return value


class JwtTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Пользователь с таким именем не найден',
        ),
    ])
