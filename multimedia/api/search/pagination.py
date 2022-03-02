from rest_framework import pagination


class SearchPagination(pagination.PageNumberPagination):
    page_size = 50
