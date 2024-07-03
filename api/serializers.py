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