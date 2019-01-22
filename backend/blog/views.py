from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Post, Subscriptions, User
from .serializers import PostSerializer, CreatePostSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class AddSubscriptionView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        response_data = {}
        author_id = request.query_params.get('author_id', None)
        if author_id is None:
            response_data['error'] = 'You need to add an author_id in request.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        elif int(author_id) == request.user.id:
            response_data['error'] = 'You cannot subscribe to yourself.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        elif not User.objects.filter(id=author_id).exists():
            response_data['error'] = 'No such author'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        author = User.objects.get(id=author_id)
        if Subscriptions.objects.filter(user=request.user, author=author).exists():
            response_data['error'] = 'You are already subscribed on this author.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscriptions.objects.create(author=author, user=request.user)
            subscription.full_clean()
            return Response(response_data, status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status.HTTP_400_BAD_REQUEST)


class DeleteSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = {}
        author_id = request.query_params.get('author_id', None)
        if author_id is None:
            response_data['error'] = 'You need to add an author_id in request.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        elif int(author_id) == request.user.id:
            response_data['error'] = 'You cannot unsubscribe to yourself.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        elif not User.objects.filter(id=author_id).exists():
            response_data['error'] = 'No such author'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        author = User.objects.get(id=author_id)
        if not Subscriptions.objects.filter(user=request.user, author=author).exists():
            response_data['error'] = 'You are already not subscribed on this author.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscriptions.objects.get(user=request.user, author=author)
            subscription.delete()
            return Response(response_data, status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status.HTTP_400_BAD_REQUEST)


class CreatePostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        # data = json.loads(request.body)
        serializer.save(author=self.request.user)


class GetMyList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def get_queryset(self):
        # authors = Subscriptions.objects.filter(user=self.request.user)
        posts = Post.objects.filter(
            author__readers__user=self.request.user).order_by('-id')
        return posts


class GetUserList(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(
            author__readers__user_id=self.kwargs['user_id']).order_by('-id')
        return posts


class MarkPost(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
            subscription = Subscriptions.objects.get(
                user=self.request.user, author=post.author)
            subscription.have_read.add(post)
            subscription.save()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
