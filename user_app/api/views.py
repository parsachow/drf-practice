from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app.api.serializers import RegistrationSerializer

@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        #since its a POST req, we are getting data from user, we will use serializer, get data from user, pass data in our serializer and '''SAVE''' it.
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)