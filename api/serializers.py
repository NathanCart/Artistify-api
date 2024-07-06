from rest_framework import serializers
from .models import Item, Location, User

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('__all__')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    def update(self, instance, validated_data):
        instance.artist_list = validated_data.get('artist_list', instance.artist_list)
        instance.spotify_id = validated_data.get('spotify_id', instance.spotify_id)
        instance.save()
        return instance