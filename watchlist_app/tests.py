from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models 


# # test methods need to be named with the keyword 'test_'

class StreamPlatformTestCase(APITestCase):
    
    # in setUp(), we created a user, logged them in, got the token and manually created a platform to use for accessing the list/individual item if a user wants to access it through get req
    def setUp(self):
        self.user = User.objects.create_user(
            username="example", 
            password="Password@123"
            )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name= "Netflix",
            about= "#1 platform for streaming",
            website= "https://netflix.com"
        )
        
    
    def test_streamplatform_create(self):
        data = {
            "name" : "Netflix",
            "about" : "#1 platform for streaming",
            "website" : "https://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data) # using streamplatform-list as we are using a router to make a post req 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #status 403 as normal user cant create a stream platform
    
    
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_streamplatform_indv(self):
         #accessing an individual item/pk, we need to pass an argument inside reverse method and the args need to hold the self id of the pk ex; self.stream.id
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchlistTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="example", 
            password="Password@123"
            )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name= "Netflix",
            about= "#1 platform for streaming",
            website= "https://netflix.com"
        )
        
        self.watchlist = models.Watchlist.objects.create(
            platform = self.stream,
            title = "Life of Pi",
            description = "a boy and his tiger",
            active = True
        )
        
        
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title":"Life of Pi",
            "description":"a boy and his tiger",
            "active": True
        }
        response = self.client.post(reverse('media-list'), data) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_watchlist_getlist(self):
        response = self.client.get(reverse('media-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_watchlist_indv(self):
        response = self.client.get(reverse('media-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.get().title, 'Life of Pi') # instead of status_code, we can also match an object through an attribute in the response


class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="example", 
            password="Password@123"
            )
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name= "Netflix",
            about= "#1 platform for streaming",
            website= "https://netflix.com"
        )
        
        self.watchlist = models.Watchlist.objects.create(
            platform = self.stream,
            title = "Life of Pi",
            description = "a boy and his tiger",
            active = True
        )
        
        # watclist2 and review data for testing update functionality
        self.watchlist2 = models.Watchlist.objects.create(
            platform = self.stream,
            title = "Death by coding",
            description = "a girl and her computer",
            active = True
        )
        self.review = models.Review.objects.create(
            review_user = self.user,
            rating = 3,
            review_desc = "scary!",
            watchlist = self.watchlist2
        )
    
    
    def test_review_create(self):
        data = {
            "review_user" : self.user,
            "rating": 3,
            "review_desc": "boringgg!",
             "watchlist": self.watchlist
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data) #accessing an individual item/pk, we need to pass an argument inside reverse method and the args need to hold the self id of the pk ex; self.stream.id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(models.Review.objects.get().rating, 3)
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data) #trying to create a 2nd review in the same movie by the same user
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_review_create_unauth(self): #unauthorized user
        data = {
            "review_user" : self.user,
            "rating": 3,
            "review_desc": "boringgg!",
             "watchlist": self.watchlist
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_review_update(self):
        data = {
            "review_user" : self.user,
            "rating": 4,
            "review_desc": "scary!- update",
             "watchlist": self.watchlist
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,))) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_review_indv(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,))) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)