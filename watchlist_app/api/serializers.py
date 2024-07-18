from rest_framework import serializers
from watchlist_app.models import Movie


def name_length(value):
  if len(value) < 2:
    raise serializers.ValidationError("Name is too short!")
  else:
    return(value)


class MovieSerializer(serializers.Serializer):
    #add in fieldtype after serializers
    #everthing will be mapped using serializer according to our models 
    id = serializers.IntegerField(read_only=True) 
    #read_only=True is used to access the id only
    
    name = serializers.CharField(validators=[name_length])
    #direct validator on the serializer field
    
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
    
    # # OBJECT LEVEL VALIDATION
    def validate(self, data):
      if data['name'] == data['description']:
        raise serializers.ValidationError("Name and Description cannot be same")
      else:
        return data
    
    
    # # FIELD LEVEL VALIDATION
    # def validate_name(self, value): 
    #   #for field level validation, the title/name of the field needs to be added to validate_
    #   #the value parameter holds the value of the field type
    #     if len(value) < 2:
    #       raise serializers.ValidationError("Name is too short")
    #     else:
    #       return(value)