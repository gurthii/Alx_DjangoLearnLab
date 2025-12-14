from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification

User = get_user_model()

def create_notification(actor, recipient, verb, target):
    """Creates a notification instance."""
    
    # 1. Do not notify if the actor is the recipient
    if actor == recipient:
        return

    # 2. Prevent duplicate notifications for non-unique events (e.g. repeated follows)
    if verb in ['followed'] and Notification.objects.filter(actor=actor, recipient=recipient, verb=verb).exists():
        return

    # 3. Create the notification
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        content_type=ContentType.objects.get_for_model(target),
        object_id=target.pk,
        target=target
    )