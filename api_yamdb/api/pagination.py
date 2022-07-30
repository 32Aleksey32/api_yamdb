from rest_framework.pagination import PageNumberPagination


class UsersPagination(PageNumberPagination):
    page_size = 5


class CategoriesPagination(PageNumberPagination):
    page_size = 3


class GenresPagination(PageNumberPagination):
    page_size = 15


class TitlesPagination(PageNumberPagination):

    page_size = 32


class ReviewsPagination(PageNumberPagination):
    page_size = 32


class CommentsPagination(PageNumberPagination):
    page_size = 32
