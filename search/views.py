from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.serializers import UserSerializer

User = get_user_model()


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '').strip()

        if not query:
            return Response(
                {'error': 'Search query is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(bio__icontains=query)
        ).exclude(id=request.user.id)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)