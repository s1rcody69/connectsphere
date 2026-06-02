from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment, PostLike, CommentLike

User = get_user_model()


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer(read_only=True)
    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content',
            'total_likes', 'is_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'post', 'created_at', 'updated_at']

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return obj.likes.filter(user=request.user).exists()
            except Exception:
                return False
        return False


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']

    def create(self, validated_data):
        request = self.context.get('request')
        post = self.context.get('post')
        return Comment.objects.create(
            author=request.user,
            post=post,
            **validated_data
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'comment', 'created_at']