from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'per_page'
    max_page_size = 50
    page_query_param = 'page_num'