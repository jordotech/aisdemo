import logging
from rest_framework import pagination
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger('api')

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000