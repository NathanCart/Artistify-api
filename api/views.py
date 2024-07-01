from rest_framework import generics
from .models import Item, Location

from .serializers import ItemSerializer, LocationSerializer

class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        querySet = Item.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            querySet = querySet.filter(itemLocation=location)
        return querySet

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()