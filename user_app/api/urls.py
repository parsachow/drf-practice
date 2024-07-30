from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration, logout

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration, name='register'),
    path('logout/', logout, name='logout'),
]
