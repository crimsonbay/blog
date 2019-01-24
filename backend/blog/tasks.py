from django.core.mail import send_mail
from .models import User
from backend.celery import app
from backend.settings import SITE_ADDRESS, EMAIL_HOST_USER


# celery task for mailing about the new post to every subscriber of given author
# time limit 1 hour
@app.task(name='shop.tasks.new_post_mail', time_limit=3600)
def new_post_mail(post_id, author_id, title):
    # email subject
    subject = 'Новый пост.'
    # email message
    message = 'Один из авторов, на которого вы подписаны, написал новый пост:\n' \
              + title + '\n'\
              + 'Прочитать его вы можете по ссылке:\n'\
              + SITE_ADDRESS + '/post/' + str(post_id) + '/'
    # list emails of subscribers
    subscribers_emails = list(User.objects
                              .filter(subscriptions__author_id=author_id)
                              .values_list('email', flat=True))
    # sending mail
    send_mail(subject, message, EMAIL_HOST_USER, subscribers_emails)
