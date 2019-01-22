from django.contrib import admin
from .models import Post, Subscriptions
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    pass

class SubscriptionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
