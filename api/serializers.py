from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    def update(self, instance, validated_data):
        instance.artists = validated_data.get('artists', instance.artists)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.friends = validated_data.get('friends', instance.friends)
        instance.spotify_id = validated_data.get('spotify_id', instance.spotify_id)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.save()
        return instance