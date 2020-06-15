from rest_framework import serializers 
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    writer = serializers.StringRelatedField()
    director = serializers.StringRelatedField()
    produced_by = serializers.StringRelatedField()

    class Meta:
        model = Movie
        fields = '__all__'