from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve notifications where the current user is the recipient
        queryset = Notification.objects.filter(recipient=self.request.user)
        
        # Optional: Mark notifications as read upon fetching
        queryset.filter(read=False).update(read=True)
        
        return queryset.order_by('-timestamp')