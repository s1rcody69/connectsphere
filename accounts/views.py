from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """
    Handle new user registration.
    Returns user data and JWT tokens on success.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Account created successfully.',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Handle user login.
    Returns JWT tokens on successful authentication.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful.',
                        'user': UserSerializer(user).data,
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'This account has been deactivated.'
                    }, status=status.HTTP_403_FORBIDDEN)

            return Response({
                'error': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """
    Handle user logout.
    Blacklists the refresh token to invalidate the session.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required.'
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Logged out successfully.'
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response({
                'error': 'Invalid or expired token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    Return the currently authenticated user's details.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
