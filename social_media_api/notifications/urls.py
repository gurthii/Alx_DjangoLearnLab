from django.urls import path
from .views import NotificationListView

urlpatterns = [
    # Route for viewing user's notifications
    path('', NotificationListView.as_view(), name='notification-list'),
]