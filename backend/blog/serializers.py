from rest_framework import serializers
from .models import Post, Subscriptions, User


class UserForPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%b %d %Y %H:%M:%S')
    author = UserForPostSerializer()
    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_at', 'readed')
