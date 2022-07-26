from rest_framework import serializers
from reviews.models import Title, Category, Genre
from rest_framework.relations import SlugRelatedField


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', read_only=True)
    genre = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
