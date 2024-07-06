from rest_framework import generics, status
from .models import Item, Location, User
from rest_framework.views import APIView
from .serializers import ItemSerializer, LocationSerializer, UserSerializer
from rest_framework.response import Response

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

class UserApiView(APIView):    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            # Retrieve a single user
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all users
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
