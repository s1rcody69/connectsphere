from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer

User = get_user_model()


class PostListCreateView(APIView):
    """
    GET  - List all posts (newest first, paginated)
    POST - Create a new post
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().select_related('author')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                PostSerializer(post, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    GET    - Retrieve a single post
    PUT    - Update a post (owner only)
    DELETE - Delete a post (owner only)
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, post_id):
        return get_object_or_404(Post, id=post_id)

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        post = self.get_object(post_id)

        if post.author != request.user:
            return Response(
                {'error': 'You can only edit your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostCreateSerializer(
            post,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                PostSerializer(post, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_object(post_id)

        if post.author != request.user:
            return Response(
                {'error': 'You can only delete your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(
            {'message': 'Post deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class UserPostsView(APIView):
    """
    GET - Retrieve all posts by a specific user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(author=user).select_related('author')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)