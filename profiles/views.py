from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Profile, Follow
from .serializers import ProfileSerializer, ProfileUpdateSerializer

User = get_user_model()


class ProfileDetailView(APIView):
    """
    Retrieve a user profile by user ID.
    Any authenticated user can view any profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    """
    Update the currently authenticated user's profile.
    Users can only update their own profile.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            full_profile = ProfileSerializer(profile)
            return Response({
                'message': 'Profile updated successfully.',
                'profile': full_profile.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(APIView):
    """
    Retrieve the currently authenticated user's own profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            return Response(
                {'message': 'You are already following this user.'},
                status=status.HTTP_200_OK
            )

        # Update follower and following counts
        target_profile = get_object_or_404(Profile, user=target_user)
        target_profile.followers_count += 1
        target_profile.save()

        my_profile = get_object_or_404(Profile, user=request.user)
        my_profile.following_count += 1
        my_profile.save()

        return Response(
            {'message': f'You are now following {target_user.username}.'},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        follow = Follow.objects.filter(follower=request.user, following=target_user)

        if not follow.exists():
            return Response(
                {'error': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow.delete()

        target_profile = get_object_or_404(Profile, user=target_user)
        if target_profile.followers_count > 0:
            target_profile.followers_count -= 1
            target_profile.save()

        my_profile = get_object_or_404(Profile, user=request.user)
        if my_profile.following_count > 0:
            my_profile.following_count -= 1
            my_profile.save()

        return Response(
            {'message': f'You have unfollowed {target_user.username}.'},
            status=status.HTTP_204_NO_CONTENT
        )
