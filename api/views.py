from rest_framework import generics, status
from .models import Item, Location, User
from rest_framework.views import APIView
from .serializers import ItemSerializer, LocationSerializer, UserSerializer
from rest_framework.response import Response
import requests

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

class UserCurrent(APIView):
    def get(self, request, *args, **kwargs):
        access_token = self.request.query_params.get('accessToken')
        r = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + access_token})
        if r.status_code == 200:
            spotify_data = r.json()
            try:
                user = User.objects.get(spotify_id=spotify_data['id'])
                user_artists = ",".join(user.artists)
                artistsRequest = requests.get('https://api.spotify.com/v1/artists?ids=' + user_artists, headers={'Authorization': 'Bearer ' + access_token})
                if artistsRequest.status_code == 200:
                    artists_data = artistsRequest.json()
                serializer = UserSerializer(user)
                combined_data = {**serializer.data, 'spotify_data': spotify_data, 'artists': artists_data['artists']}
                return Response(combined_data)
            except User.DoesNotExist:
                return Response({"error": "User not found in the database"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Unable to fetch data from Spotify"}, status=status.HTTP_400_BAD_REQUEST)

class AddArtist(APIView):
    def post(self, request, *args, **kwargs):
        spotify_id = request.data['spotifyId']
        artist_id = request.data['artistId']
        user = User.objects.get(spotify_id=spotify_id)
        serializer = UserSerializer(user)

        if artist_id in user.artists:
            return Response({"error": "Artist already in list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.artists.append(artist_id)
            user.save()
            return Response(serializer.data)

class UserApiView(APIView):    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            # Retrieve a single user
            try:
                if pk.isnumeric():
                    user = User.objects.get(pk=pk)
                else:
                    user = User.objects.get(spotify_id=pk)
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
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        if pk.isnumeric():
            user = User.objects.get(pk=pk)
        else:
            user = User.objects.get(spotify_id=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pk = self.kwargs.get('pk')
        if pk.isnumeric():
            user = User.objects.get(pk=pk)
        else:
            user = User.objects.get(spotify_id=pk)
        try:
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)