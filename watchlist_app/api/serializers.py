from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    #add in fieldtype after serializers
    #everthing will be mapped using serializer according to our models 
    id = serializers.IntegerField(read_only=True) #read_only=True is used to access the id only
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()