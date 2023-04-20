from django.contrib import admin
from .models import Post, Like, Comment, Like_for_comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Like_for_comment)
