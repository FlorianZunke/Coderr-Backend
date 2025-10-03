from rest_framework.pagination import PageNumberPagination



class OffersResultPagination(PageNumberPagination):
    """
    Custom pagination class for offers with a default page size of 2.
    Allows clients to specify a custom page size via the 'page_size' query parameter,
    up to a maximum of 10,000.
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000