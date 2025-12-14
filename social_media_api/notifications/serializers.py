from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Display the actor's username
    actor_username = serializers.ReadOnlyField(source='actor.username')
    # Display the type of object that was acted upon (e.g., 'Post', 'User')
    target_type = serializers.CharField(source='target.__class__.__name__', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 'timestamp', 'read', 'target_type']
        read_only_fields = ['recipient', 'actor', 'verb', 'timestamp', 'read', 'content_type', 'object_id']