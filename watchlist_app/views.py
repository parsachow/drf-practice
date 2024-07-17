# from django.shortcuts import render
# from .models import Movie
# #helps get response in the form of JSON
# from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all() 
#     data = {
#         'movies' : list(movies.values()) #'.values()' method returns quesryset in the form of a dictionary
#     }
     
#     return JsonResponse(data)

# #(when a user makes a request) everytime we make an entry, we are creating a Model oject which are complex datatypes. when we fetch/get the quesryset, its in a complex datatype which we convert to a python native datatype(python dictionary). This process is known as SERIALIZATION. and the opposite process is known as DESERIALIZATION. Then we render it into json data which is returned to the user and vice versa.
    
# def movie_detail(request, pk): #getting a specific object by passing a pk
#     movie = Movie.objects.get(pk=pk)
#     #print(movie)
#     data = {
#         'name' : movie.name,
#         'description' : movie.description,
#         'active' : movie.active
#     }
    
#     return JsonResponse(data)
    