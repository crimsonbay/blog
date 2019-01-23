from rest_framework import serializers
from .models import Post, Subscription, User


# little serializer for author in PostSerializer
class UserForPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


# for post creation serializer
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')


# main serializer for Post
class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%b %d %Y %H:%M:%S')
    author = UserForPostSerializer()
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created_at')


class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    class Meta:
        model = Subscription
        fields = ('user',)
