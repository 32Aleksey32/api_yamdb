import datetime as dt

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Genre, User, Review, Comment


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
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


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
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Not a valid username.',
        )
    ])

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Using "me" as a username is forbidden.')
        return value


class JwtTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='A user with that username is not found.',
        )
    ])


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)
