from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    
    #test methods need to be named with the keyword 'test_'
    def test_register(self):
        
        #get data, send a post req, get response, check response, throw error if response is incorrect. 
        #Main Database is NOT utlized while executing testcases. Django creates temp DB for tests
        data = {
            "username" : "testcase",
            "email" : "test@testcase.com",
            "password" : "NewPassword@123",
            "password2" : "NewPassword@123"
        }
        #sending client post request. Need to pass URL(using reverse and using the name of the url we are testing) and DATA
        response = self.client.post(reverse('register'), data) #sending data to the register link
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #checking to see if we created the new user with the above data


class LoginLogoutTestCase(APITestCase):
    
    #create user and test login/logout functionality. #setup class to create user for this particular TC
    def setUp(self):
        self.user = User.objects.create_user(
            username='example', 
            password='NewPassword@123'
        )
        
    
    def test_login(self):
        data = {
            "username" : "example",
            "password" : "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_logout(self):
        #to logout first we need user Token. same to post reviews etc, store in self.token. send req to logout link.
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    