from rest_framework.decorators import api_view 
from rest_framework.views import APIView 
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters


from django.shortcuts import get_object_or_404

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.throtlling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchlistPagination


# # Create your views here.
#django-filter pkg only works on Generic views

# # Model Viewset

# ModelVs lets us access everything including(get,post,put,delete) while ReadOnlyModelVs lets us access only get method

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]


# # Viewset

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     def destroy(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# # Concrete CBV 

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        # username = self.kwargs['username'] # directly mapping value of username
        # return Review.objects.filter(review_user__username=username) #filtering against URL. Bc review_user is a Foreign Key in the Review models, we need to pass 1 dunder after review_user to get inside the field and get the specific attribute. if it was not a FK, then we could directly use - review_user = username / rating = username etc
        
        username = self.request.query_params.get('username', None) # using query params to filter through username
        #query params only match with exactly same values
        return Review.objects.filter(review_user__username=username) 
        
        
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # object level permissions
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    throttle_classes = [ReviewListThrottle, AnonRateThrottle] #throttles are counted ALL together
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rating'] #as review_user is a FK, we need to access the username like shown above instead of directly accessing it like 'rating'
    
    def get_queryset(self): #overriding queryset to get a specific item
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk) #filtering object according to the movie we want


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk') 
        media = Watchlist.objects.get(pk=pk)
        
        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=media, review_user=user) #filtering through 2 criterias(media and user)to see if user already left review in this particular media
        if review_queryset.exists():
            raise ValidationError("Oops you already left a review!")
        
        if media.num_of_reviewer == 0:
            media.avg_rating = serializer.validated_data['rating']
        else:
            media.avg_rating = (media.avg_rating + serializer.validated_data['rating']) /2
        
        media.num_of_reviewer = media.num_of_reviewer +1
        media.save() #save the instance
        
        # if we want to add any other funtionality then we add them above, before calling serializer.save
        serializer.save(watchlist=media, review_user=user)
        
        # return super().perform_create(serializer)
    
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    # custom throttle for individual class to restrict specific parts of api
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    

# # Mixins - helps provide basic view behaviors without defining them in detail. We define a queryset along with the method we need.

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView): #genericApiView will always be at the end after all the mixins
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)



# # CBVs

# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True)
#         return Response(serializer.data)
    
    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StreamPlatformDetails(APIView):
#     def get(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error' : 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 
        
                
class WatchListFilterTest(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    pagination_class = WatchlistPagination
    
    # filter_backends = [DjangoFilterBackend] #good for working with specific values like rating, exact matches only as using params
    # filterset_fields = ['title', 'platform__name']
    
    filter_backends = [filters.SearchFilter] #search filter will provide ALL results with info entered into search bar
    search_fields = ['title', 'platform__name'] 


    # filter_backends = [filters.OrderingFilter] #order by ascending/descending 
    # ordering_fields = ['title', 'avg_rating'] 

                
class WatchlistAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request): #pass in request as the 2nd parameter in CBV
        medialist = Watchlist.objects.all() #get all medias
        #create a variable ex; serialiser to store all the data about the ex; medias and pass medias as complex data into the serializer class 
        
        serializer = WatchlistSerializer(medialist, many=True) #When using GET request to fetch ALL objects/data, use - many=True as the 2nd argument
    
        #return a Response. Pass the variable  created to store the data ex; serializer.data as the response
        return Response(serializer.data)
    
    def post(self, request):
        
        #since its a POST req, we are getting data from user, we will use serializer, get data from user and '''SAVE''' it.
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchlistDetail(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            media = Watchlist.objects.get(pk=pk) #passing pk=pk as we are getting a specific item
        except Watchlist.DoesNotExist:
            # sending response in the form of json dictionary
            return Response({'Error' : 'Media not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchlistSerializer(media)
        return Response(serializer.data)
    
    def put(self, request, pk):
        media = Watchlist.objects.get(pk=pk) #passing pk=pk as we are UPDATING a specific item
        serializer = WatchlistSerializer(media, data=request.data) #pass media in serializer so it updates that specific pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        media = Watchlist.objects.get(pk=pk) #passing pk=pk as we are DELETING a specific item
        media.delete() #regular quearyset, no serialization involved
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        

# # function based views of the above CBVs

# @api_view(['GET', 'POST']) #By default, it only provides GET req
# #decorator for working with function based views which provides some functionality like receiving Request or adding context to Response. 
# def movie_list(request):
#     if request.method == 'GET':
        
#         movies = Movie.objects.all() #get all movies
#         #create a variable ex; serialiser to store all the data about the ex; movies and pass movies as complex data into the serializer class 
        
#         serializer = MovieSerializer(movies, many=True) #When using GET request to fetch all objects/data, use - many=True as the 2nd argument
    
#         #return a Response. Pass the variable  created to store the data ex; serializer.data as the response
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         #since its a POST req, we are getting data from user, we will use serializer, get data from user, pass data into serializer and '''SAVE''' it.
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET', 'PUT', 'DELETE'])
# #PUT/DELETE Req can only be performed on individual items. PATCH req will only update specific fields on an item not the whole thing like PUT. 

# def movie_detail(request, pk): #getting a specific object by passing a pk
    # if request.method == 'GET':
        
    #     # check if pk exists or not through try/except block and send error msg depending on it. Otherwise move to serializer
    #     try:
    #         movie = Movie.objects.get(pk=pk) #passing pk=pk as we are getting a specific item
    #     except Movie.DoesNotExist:
    #         # sending response in the form of json dictionary
    #         return Response({'Error' : 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = MovieSerializer(movie)
    #     return Response(serializer.data)
    
    # elif request.method == 'PUT':
    #     movie = Movie.objects.get(pk=pk) #passing pk=pk as we are UPDATING a specific item
    #     serializer = MovieSerializer(movie, data=request.data) #pass movie in serializer so it updates that specific pk
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'DELETE':
    #     movie = Movie.objects.get(pk=pk) #passing pk=pk as we are DELETING a specific item
    #     movie.delete() #regular quearyset, no serialization involved
    #     return Response(status=status.HTTP_204_NO_CONTENT)