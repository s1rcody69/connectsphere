from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'website', 'followers_count', 'following_count', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at']
