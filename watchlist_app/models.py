from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name

class Watchlist(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    # 1 platform can have many medias, so 1:M relationship, so add FK
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist') 
    
    def __str__(self):
        return self.title

class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_desc = models.TextField(max_length=300, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    reviews = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        return f'{self.rating} - {self.reviews.title}'