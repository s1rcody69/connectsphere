from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Profile
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
