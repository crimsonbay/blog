"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog.views import AddSubscriptionView, CreatePostView, GetMyList, GetUserList,\
    MarkPost, DeleteSubscriptionView, GetAllMyList, index, UserView,\
    SubscriptionView, NoSubscriptionView, post_list, post_list_all, AllPosts, feed,\
    post_view, PostView, user_list, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view()),
    path('list/', post_list, name='list'),
    path('list_all/', post_list_all, name='list_all'),
    path('list/<int:user_id>/', user_list, name='user_list'),
    path('feed/', feed, name='feed'),
    path('post/<int:post_id>/', post_view, name='post_view'),
    path('api/post/<int:post_id>/', PostView.as_view()),
    path('admin/', admin.site.urls),
    path('api/subscribe/<int:author_id>/', AddSubscriptionView.as_view()),
    path('api/unsubscribe/<int:author_id>/', DeleteSubscriptionView.as_view()),
    path('api/create-post/', CreatePostView.as_view()),
    path('api/list/', GetMyList.as_view()),
    path('api/list-all/', GetAllMyList.as_view()),
    path('api/feed/', AllPosts.as_view()),
    path('api/list/<int:user_id>/', GetUserList.as_view()),
    path('api/mark-read/<int:post_id>/', MarkPost.as_view()),
    path('api/users/', UserView.as_view()),
    path('api/subscriptions/', SubscriptionView.as_view()),
    path('api/nosubscriptions/', NoSubscriptionView.as_view()),
    re_path(r'^$', index, name='index'),
]

urlpatterns += [
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]