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
    SubscriptionView, NoSubscriptionView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^$', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/subscribe/<int:author_id>/', AddSubscriptionView.as_view()),
    path('api/unsubscribe/<int:author_id>/', DeleteSubscriptionView.as_view()),
    path('api/create-post/', CreatePostView.as_view()),
    path('api/list/', GetMyList.as_view()),
    path('api/list_all/', GetAllMyList.as_view()),
    path('api/list/<int:user_id>/', GetUserList.as_view()),
    path('api/mark-read/<int:post_id>/', MarkPost.as_view()),
    path('api/users/', UserView.as_view()),
    path('api/subscriptions/', SubscriptionView.as_view()),
    path('api/nosubscriptions/', NoSubscriptionView.as_view()),
]

urlpatterns += [
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]