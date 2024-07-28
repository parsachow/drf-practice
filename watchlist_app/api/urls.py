from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import ReviewCreate, ReviewDetail, ReviewList, WatchlistAV, WatchlistDetail, StreamPlatformAV, StreamPlatformDetails

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_detail, name='movie-detail'),
    
    path('list/', WatchlistAV.as_view(), name='media-list'),
    path('list/<int:pk>/', WatchlistDetail.as_view(), name='media-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='platform-list'),
    path('stream/<int:pk>/', StreamPlatformDetails.as_view(), name='platform-detail'),
    
    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    path('list/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'), 
    path('list/<int:pk>/review/', ReviewList.as_view(), name='review-list'), #all reviews for a specific item
    path('list/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')
]