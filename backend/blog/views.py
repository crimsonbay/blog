from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Post, Subscription, User, ReadPost
from .serializers import PostSerializer, CreatePostSerializer, UserMiniSerializer,\
    SubscriptionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse

# Create your views here.


# '/api/subscribe/<int:author_id>' subscription on author view
class AddSubscriptionView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        response_data = {}
        author_id = self.kwargs['author_id']
        # if no author in request - error
        if author_id is None:
            response_data['error'] = 'You need to add an author_id in request.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # if trying subscribe to yourself - error
        elif author_id == request.user.id:
            response_data['error'] = 'You cannot subscribe to yourself.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # if no such author in DB - error
        elif not User.objects.filter(id=author_id).exists():
            response_data['error'] = 'No such author'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        author = User.objects.get(id=author_id)
        # if subscription already exists, nothing to delete - error
        if Subscription.objects.filter(user=request.user, author=author).exists():
            response_data['error'] = 'You are already subscribed on this author.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # create subscription
        try:
            subscription = Subscription.objects.create(author=author, user=request.user)
            subscription.full_clean()
            return Response(response_data, status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status.HTTP_400_BAD_REQUEST)


# 'api/unsubscribe/<int:author_id>' unsubscription on author view
class DeleteSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = {}
        author_id = self.kwargs['author_id']
        # if no author in request - error
        if author_id is None:
            response_data['error'] = 'You need to add an author_id in request.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # if trying subscribe to yourself - error
        elif author_id == request.user.id:
            response_data['error'] = 'You cannot unsubscribe to yourself.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # if no such author in DB - error
        elif not User.objects.filter(id=author_id).exists():
            response_data['error'] = 'No such author'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        author = User.objects.get(id=author_id)
        # if no subscription, nothing to delete - error
        if not Subscription.objects.filter(user=request.user, author=author).exists():
            response_data['error'] = 'You are already not subscribed on this author.'
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        # delete subscription
        try:
            Subscription.objects.get(user=request.user, author=author).delete()
            return Response(response_data, status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status.HTTP_400_BAD_REQUEST)


# 'api/create-post/' creates new post with authenticated user and data in body
class CreatePostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 'api/feed/' get list of ALL posts ALL users
class AllPosts(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.all().order_by('-id')
        return posts

# 'api/list/' get list of posts from user subscriptions for authenticated user
# WITHOUT posts had read
class GetMyList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def get_queryset(self):
        print(self.request.user)
        posts = Post.objects.filter(
            Q(author__readers__user_id=self.request.user) &
            ~Q(user_read__user_id=self.request.user)).order_by('-id')
        return posts


# 'api/list_all/' get list of posts from user subscriptions for authenticated user
# WITH posts had read
class GetAllMyList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(
            author__readers__user_id=self.request.user).order_by('-id')
        return posts


# 'api/list/<int:user_id>/' get list of posts for specified user
class GetUserList(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(
            author__readers__user_id=self.kwargs['user_id']).order_by('-id')
        return posts


# 'api/mark-read/<int:post_id>/' marks post as read for authenticated user
# if no subscription on this author then error, user can mark only subscribed authors
# posts
class MarkPost(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        # if post already marked - error
        if ReadPost.objects.filter(post_id=self.kwargs['post_id']).exists():
            response_data['error'] = 'Already read.'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # if no subscription on this author - error
        elif not Subscription.objects.filter(
                user=self.request.user,
                author__posts=self.kwargs['post_id']).exists():
            response_data['error'] =\
                'You can not tag this post because it is not subscribed to its author'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # create mark
        try:
            ReadPost.objects.create(user=self.request.user,
                                    post_id=self.kwargs['post_id'])
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# 'api/users/' return ALL Users WITH authenticated if user is_authenticated
class UserView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users


# 'api/subscriptions/' return all authors user have subscribed without authenticated user
class SubscriptionView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        users = User.objects.filter(Q(readers__user_id=self.request.user) &
                                    ~Q(id=self.request.user.id))
        return users


# 'api/nosubscriptions/' return all authors user have NOT subscribed without authenticated user
class NoSubscriptionView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        users = User.objects.filter(
            ~Q(readers__user_id=self.request.user) &
            ~Q(id=self.request.user.id))
        return users


# 'api/post/<int:post_id>/' return post by post.id
class PostView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        response_data = {}
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
            response_data = PostSerializer(post).data
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# HORRORS OF THE FRONTEND


# index page with subscriptions and nonsubscriptions
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


# list of NOT READ posts of the user page
@login_required(login_url='/login/')
def post_list(request):
    return render(request, 'list.html')

# list of ALL posts of the user page
@login_required(login_url='/login/')
def post_list_all(request):
    return render(request, 'list_all.html')


# list of ALL posts of ALL users page
def feed(request):
    return render(request, 'feed.html')


# the certain post page
def post_view(request, *args, **kwargs):
    post_id = kwargs['post_id']
    context = {'post_id': post_id}
    return render(request, 'post.html', context=context)


# the list of all subscribed posts of certain user by user.id
def user_list(request, *args, **kwargs):
    user_id = kwargs['user_id']
    context = {'user_id': user_id}
    return render(request, 'user_list.html', context=context)


# 'api/logout/' api-call for logout user
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.user.is_authenticated:
            logout(request)
        return Response(response_data, status=status.HTTP_200_OK)
