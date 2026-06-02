from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostAuthorSerializer(serializers.ModelSerializer):
    """
    Minimal user serializer for embedding author info inside post responses.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']


class PostSerializer(serializers.ModelSerializer):
    """
    Full post serializer for reading post data.
    Includes author details, like count, and comment count.
    """

    author = PostAuthorSerializer(read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'image',
            'hashtags',
            'total_likes',
            'total_comments',
            'is_liked',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()

    def get_is_liked(self, obj):
       request = self.context.get('request')
       if request and request.user.is_authenticated:
        try:
            return obj.likes.filter(user=request.user).exists()
        except Exception:
            return False
       return False
    
class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating posts.
    Author is set automatically from the request user.
    """

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'hashtags']

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(
            author=request.user,
            **validated_data
        )
        return post