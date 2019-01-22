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
from django.urls import path, re_path
from blog.views import AddSubscriptionView, CreatePostView, GetMyList, GetUserList,\
    MarkPost, DeleteSubscriptionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscribe/', AddSubscriptionView.as_view()),
    path('unsubscribe/', DeleteSubscriptionView.as_view()),
    path('create-post/', CreatePostView.as_view()),
    path('list/', GetMyList.as_view()),
    path('list/<int:user_id>/', GetUserList.as_view()),
    path('mark-read/<int:post_id>', MarkPost.as_view()),
]
