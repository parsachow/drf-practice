from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Reviews


# # Hyperlinked Model serializer class - similiar to Model serializer class except uses hyperlinks to represent relationships instead of pk
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reviews
    fields = '__all__'



# # Model serializer class - default fields are automatically populated, defualt '.create()' & '.update()' implementation methods are provaided

class WatchlistSerializer(serializers.ModelSerializer):
  #Nested serializer. field name needs to match related_name in models
  reviews = ReviewSerializer(many=True, read_only=True)
  
  class Meta:
    model = Watchlist
    fields = "__all__"
    # if we want specific fields - 2 options
    # fields = ['id', 'name', 'active'] 
    # OR, 
    # exclude = ['description']
  
  
  # # OBJECT LEVEL VALIDATION
  def validate(self, data):
    if data['name'] == data['description']:
      raise serializers.ValidationError("Name and Description cannot be same")
    else:
      return data
    
    
  # FIELD LEVEL VALIDATION
  def validate_name(self, value):
    #for field level validation, the title/name of the field needs to be added to validate_
    
    #the value parameter holds the value of the field type
    if len(value) < 2:
      raise serializers.ValidationError("Name is too short")
    else:
      return(value)
    
    
  
class StreamPlatformSerializer(serializers.ModelSerializer):
  # Nested serializer. field name needs to be the exact same as the 'related_name in models.py'
  watchlist = WatchlistSerializer(many=True, read_only=True)  
  #one streaming platform can have many medias.
  #needs to be placed under the serializer being used here
  
  class Meta:
    model = StreamPlatform
    fields = "__all__"
  
  #watchlist = serializers.StringRelatedField(many=True)
  #another option for nested serializer realtionship.utilize our models and return __str__
  #other options include PKrelatedfield, HyperlinkedIdentityField-to access object URL like ID/desc etc, HyperlinkedRelatedField
  #watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='')
  #we also need to pass 'context={'request':request}' when initilizing serializer in views.py
  
    
    

# def name_length(value):
#   if len(value) < 2:
#     raise serializers.ValidationError("Name is too short!")
#   else:
#     return(value)



# # regular serializer class - manually populate fields, manually validate, manually provide .create() & .update() methods

# class WatchlistSerializer(serializers.Serializer):
#     #add in fieldtype after serializers
#     #everthing will be mapped using serializer according to our models 
#     id = serializers.IntegerField(read_only=True) 
#     #read_only=True is used to access the id only
    
#     title = serializers.CharField(validators=[name_length])
#     #direct validator on the serializer field
    
#     description = serializers.CharField(style={'type': 'textarea'})
    
#     active = serializers.BooleanField()
    
#     #for POST request - to create data
#     def create(self, validated_data):
#         # Create and return a new `Movie` instance, given the validated data.
#       return Watchlist.objects.create(**validated_data)
  
#     def update(self, instance, validated_data): 
#         #when using UPDATE, instance carries the old value and validated data carries the new data sent by the user
        
#         instance.name = validated_data.get('name', instance.name)
#         #need to pass old instance as the 2nd argument for the validated data as its now being updated with new information
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
        
#         instance.save()
#         return instance
    