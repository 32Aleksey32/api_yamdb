from rest_framework.pagination import PageNumberPagination


class UsersPagination(PageNumberPagination):
    page_size = 5
