from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer

# # Create your views here.

@api_view(['GET', 'POST']) #By default, it only provides GET req
#decorator for working with function based views which provides some functionality like receiving Request or adding context to Response. 
def movie_list(request):
    if request.method == 'GET':
        
        movies = Movie.objects.all() #get all movies
        #create a variable ex; serialiser to store all the data about the ex; movies and pass movies as complex data into the serializer class 
        
        serializer = MovieSerializer(movies, many=True) #When using GET request to fetch all objects/data, use - many=True as the 2nd argument
    
        #return a Response. Pass the variable  created to store the data ex; serializer.data as the response
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #since its a POST req, we are getting data from user, we will use serializer, get data from user and '''SAVE''' it.
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
#PUT/DELETE Req can only be performed on individual items. PATCH req will only update specific fields on an item not the whole thing like PUT. 

def movie_detail(request, pk): #getting a specific object by passing a pk
    if request.method == 'GET':
        
        # check if pk exists or not through try/except block and send error msg depending on it. Otherwise move to serializer
        try:
            movie = Movie.objects.get(pk=pk) #passing pk=pk as we are getting a specific item
        except Movie.DoesNotExist:
            # sending response in the form of json dictionary
            return Response({'Error' : 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        movie = Movie.objects.get(pk=pk) #passing pk=pk as we are UPDATING a specific item
        serializer = MovieSerializer(movie, data=request.data) #pass movie in serializer so it updates that specific pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk) #passing pk=pk as we are DELETING a specific item
        movie.delete() #regular quearyset, no serialization involved
        return Response(status=status.HTTP_204_NO_CONTENT)