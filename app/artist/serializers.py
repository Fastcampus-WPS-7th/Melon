from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Artist, ArtistYouTube


class ArtistYouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistYouTube
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(many=True, read_only=True)
    youtube_videos = ArtistYouTubeSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'
