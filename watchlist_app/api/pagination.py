from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 5
    # page_query_param = 'pg' #name of the string we use for query param. it shows as pg instead of 'page'
    #npage_size_query_param = 'size' #customize how many reposnses can be seen by user
    max_page_size = 10
    last_page_strings = 'last' 
    
    
# class WatchlistLOPagination(LimitOffsetPagination):
#     default_limit = 5
#     max_limit = 10
#     limit_query_param = 'limit'
#     offset_query_param = 'start'


# class WatchlistCursonPagination(CursorPagination):
#     page_size = 5 #check that only 1 filter/param is active in the cbv function where this is being used
#     ordering = 'created' #overriding default parameter which is '-created' to order items from old to new