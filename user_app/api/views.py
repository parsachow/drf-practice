from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app import models
from user_app.api.serializers import RegistrationSerializer


@api_view(['POST',])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete() #current logged in user - access current token then delete it
        return Response(status=status.HTTP_200_OK)
    


@api_view(['POST',])
def registration(request):
    if request.method == 'POST':
        #since its a POST req, we are getting data from user, we will use serializer, get data from user, pass data in our serializer and '''SAVE''' it.
        serializer = RegistrationSerializer(data=request.data)
        
        data = {} #store acc data here
        
        #if serializer data is valid, we access the account info and store it in the data dictionary we made above
        if serializer.is_valid(): 
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key #access token 
            data['token'] = token #storing token here
        
        else: 
            data = serializer.errors
        
        #return response 'data' with all the saved information from above 
        return Response(data, status=status.HTTP_201_CREATED)