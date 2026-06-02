from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).select_related('sender', 'recipient')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()
        return Response(
            {'message': 'Notification marked as read.'},
            status=status.HTTP_200_OK
        )


class NotificationMarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        return Response(
            {'message': 'All notifications marked as read.'},
            status=status.HTTP_200_OK
        )