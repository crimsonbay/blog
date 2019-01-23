from django.contrib import admin
from .models import Post, Subscription, ReadPost
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    pass


class ReadPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ReadPost, ReadPostAdmin)
