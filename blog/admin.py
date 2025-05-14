from django.contrib import admin
from .models import Post, Comment, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_date', 'published_date', 'is_published']
    list_filter = ['is_published', 'published_date', 'tags']
    search_fields = ['title', 'content', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ['user', 'signature']
    filter_horizontal = ['tags']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_date', 'approved']
    list_filter = ['approved', 'created_date']
    search_fields = ['text', 'author__username', 'post__title']
    date_hierarchy = 'created_date'
