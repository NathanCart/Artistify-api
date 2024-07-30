from rest_framework import generics, status
from .models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
import requests


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
                else:
                    artists_data = {'artists': []}
                serializer = UserSerializer(user)
                combined_data = {**serializer.data, 'spotify_data': spotify_data, 'artists': artists_data['artists']}
                return Response(combined_data)
            except User.DoesNotExist:
                return Response({"error": "User not found in the database"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Unable to fetch data from Spotify"}, status=status.HTTP_400_BAD_REQUEST)

class UserFriends(APIView):
    def get(self, request, *args, **kwargs):
        spotify_id = self.request.query_params.get('spotifyId')
        user = User.objects.get(spotify_id=spotify_id)
        
        friends = User.objects.filter(id__in=user.friends)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)
    
class AddArtist(APIView):
    def post(self, request, *args, **kwargs):
        spotify_id = request.data['spotifyId']
        artist_id = request.data['artistId']
        user = User.objects.get(spotify_id=spotify_id)
        serializer = UserSerializer(user)

        if artist_id in user.artists:
            return Response({"error": "Artist already in list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.artists.insert(0, artist_id)
            user.save()
            return Response(serializer.data)

class RemoveArtist(APIView):
    def delete(self, request, *args, **kwargs):
        spotify_id = request.data['spotifyId']
        artist_id = request.data['artistId']

        print(spotify_id, artist_id, 'delete data')
        user = User.objects.get(spotify_id=spotify_id)
        serializer = UserSerializer(user)

        if artist_id in user.artists:
            user.artists.remove(artist_id)
            user.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Artist not in list"}, status=status.HTTP_400_BAD_REQUEST)

class AddFriend(APIView):
    def post(self, request, *args, **kwargs):
        spotify_id = request.data['spotifyId']
        friend_id = request.data['friendId']
        user = User.objects.get(spotify_id=spotify_id)
        serializer = UserSerializer(user)

        if friend_id in user.friends:
            return Response({"error": "Friend already in list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.friends.insert(0, friend_id)
            user.save()
            return Response(serializer.data)

class RemoveFriend(APIView):
    def delete(self, request, *args, **kwargs):
        spotify_id = request.data['spotifyId']
        friend_id = request.data['friendId']

        user = User.objects.get(spotify_id=spotify_id)
        serializer = UserSerializer(user)

        if friend_id in user.friends:
            user.friends.remove(friend_id)
            user.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Friend not in list"}, status=status.HTTP_400_BAD_REQUEST)

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
            search = request.query_params.get('search')
            queryset = User.objects.filter(display_name__icontains=search)
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