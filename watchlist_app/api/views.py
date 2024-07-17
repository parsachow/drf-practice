from rest_framework.decorators import api_view
from rest_framework.response import Response
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer

# # Create your views here.

@api_view() #By default, it only provides GET req
#decorator for working with function based views which provides some functionality like receiving Request or adding context to Response. 
def movie_list(request):
    movies = Movie.objects.all() #get all movies
    
    #create a variable ex; serialiser to store all the data about the ex; movies and pass movies as complex data into the serializer class 
    serializer = MovieSerializer(movies, many=True) #When using GET request to fetch all objects/data, use - many=True as the 2nd argument
    
    #return a Response. Pass the variable  created to store the data ex; serializer.data as the response
    return Response(serializer.data)
    

@api_view()
def movie_detail(request, pk): #getting a specific object by passing a pk
    movie = Movie.objects.get(pk=pk) #passing pk=pk as we are getting a specific item
    serializer = MovieSerializer(movie)
    return Response(serializer.data)