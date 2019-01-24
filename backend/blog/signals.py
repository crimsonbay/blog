from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Subscription, ReadPost, Post, User
from .tasks import new_post_mail


# delete all mark read associated with the subscription
@receiver(pre_delete, sender=Subscription, )
def delete_read_posts(sender, instance=None, **kwargs):
    ReadPost.objects.filter(
        user=instance.user,
        post__author=instance.author).delete()


# call celery task with mailing about new post created
# to all subscribers of this author of the post
@receiver(post_save, sender=Post)
def create_post(sender, instance=None, created=False, **kwargs):
    if created:
        new_post_mail.delay(post_id=instance.id,
                            author_id=instance.author_id, title=instance.title)
