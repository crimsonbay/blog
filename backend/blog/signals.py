from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Subscription, ReadPost

@receiver(pre_delete, sender=Subscription, )
def delete_read_posts(sender, instance=None, **kwargs):
    ReadPost.objects.filter(
        user=instance.user,
        post__author=instance.author).delete()
