from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserFeedView

# Create a router for the PostViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet)

# Create a separate router for the CommentViewSet (optional, but clean)
comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet)


urlpatterns = [
    # Main post routes (list, create, retrieve, update, delete)
    # Accessible via /api/v1/posts/
    path('', include(router.urls)),

    # Comment routes (separate for simplicity)
    # Accessible via /api/v1/comments/
    path('', include(comment_router.urls)),
    path('feed/', UserFeedView.as_view(), name='user-feed'),
]