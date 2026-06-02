from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at', 'total_likes', 'total_comments']
    search_fields = ['author__username', 'content', 'hashtags']
    readonly_fields = ['created_at', 'updated_at']
