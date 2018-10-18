from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # PageNumberPagination 默认提供的参数 有些不能满足我们的需求,我们可以通过继承来重写
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20