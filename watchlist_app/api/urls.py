from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import UserReview, ReviewCreate, ReviewDetail, ReviewList, WatchlistAV, WatchlistDetail, StreamPlatformVS


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform' )

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_detail, name='movie-detail'),
    
    path('list/', WatchlistAV.as_view(), name='media-list'),
    path('<int:pk>/', WatchlistDetail.as_view(), name='media-detail'),
    
    #for simple 'get' requests for all/individual objects we can use router and viewsets and it will get/create List as well as get individual element
    path('', include(router.urls)),
    
    # path('stream/', StreamPlatformAV.as_view(), name='platform-list'),
    # path('stream/<int:pk>/', StreamPlatformDetails.as_view(), name='platform-detail'),
    
    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    #for custom requirements, better to go with url patterns below and generic views
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'), 
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'), 
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReview.as_view(), name='user-review-detail'),
]