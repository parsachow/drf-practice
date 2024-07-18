from rest_framework import serializers
from watchlist_app.models import Movie

class MovieSerializer(serializers.Serializer):
    #add in fieldtype after serializers
    #everthing will be mapped using serializer according to our models 
    id = serializers.IntegerField(read_only=True) #read_only=True is used to access the id only
    name = serializers.CharField()
    description = serializers.CharField(style={'type': 'textarea'})
    active = serializers.BooleanField()
    
    #for POST request - to create data
    def create(self, validated_data):
        # Create and return a new `Movie` instance, given the validated data.
      return Movie.objects.create(**validated_data)
  
    def update(self, instance, validated_data): 
        #when using UPDATE, instance carries the old value and validated data carries the new data sent by the user
        
        instance.name = validated_data.get('name', instance.name)
        #need to pass old instance as the 2nd argument for the validated data as its now being updated with new information
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        
        instance.save()
        return instance