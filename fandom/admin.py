from django.contrib import admin
from .models import Profile, Post, Discussion, Comment, Fanfic


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_character', 'created_at']
    search_fields = ['user__username', 'favorite_character']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'total_likes']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'views']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'discussion', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']


@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'rating', 'genre', 'created_at', 'views', 'total_likes']
    list_filter = ['rating', 'genre', 'created_at', 'author']
    search_fields = ['title', 'description', 'author__username']

