
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from posts.models import Post
from .models import Comment, PostLike, CommentLike
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post).select_related('author')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentCreateSerializer(
            data=request.data,
            context={'request': request, 'post': post}
        )
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                CommentSerializer(comment, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return Response(
                {'error': 'You can only edit your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentCreateSerializer(
            comment, data=request.data, partial=True,
            context={'request': request, 'post': comment.post}
        )
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                CommentSerializer(comment, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return Response(
                {'error': 'You can only delete your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response({'message': 'Comment deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'message': 'You already liked this post.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        PostLike.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            return Response({'message': 'You already liked this comment.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Comment liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        CommentLike.objects.filter(user=request.user, comment=comment).delete()
        return Response({'message': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
