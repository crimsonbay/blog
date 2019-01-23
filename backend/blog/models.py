from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Post table
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=20, default='(Без названия)')
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)


# Subscriptions table, every subscription has it's own have_read posts
class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name='Подписчик',
                             on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE, related_name='readers')


class ReadPost(models.Model):
    user = models.ForeignKey(User, verbose_name='Читатель',
                             on_delete=models.CASCADE, related_name='read')
    post = models.ForeignKey(Post, verbose_name='Пост',
                             on_delete=models.CASCADE, related_name='user_read')