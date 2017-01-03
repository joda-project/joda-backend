from rest_framework_json_api import pagination


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000
