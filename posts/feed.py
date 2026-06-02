from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.models import Follow
from .models import Post
from .serializers import PostSerializer


class NewsFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list('following', flat=True)

        posts = Post.objects.filter(
            author__in=following_users
        ).select_related('author').order_by('-created_at')

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)