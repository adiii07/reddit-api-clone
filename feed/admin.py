from django.contrib import admin
from feed.models import Post, Reply, Vote

# Register your models here.
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Vote)