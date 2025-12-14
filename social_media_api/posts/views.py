from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Import the new permission class

# --- 1. Post ViewSet ---
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Require authentication for all actions
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    # --- Step 5: Pagination and Filtering ---
    # Implement filtering by title and content
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'created_at'] # Can filter by author
    search_fields = ['title', 'content'] # Can search by title and content
    ordering_fields = ['created_at', 'title'] # Can order results

    # Automatically set the author of the post to the currently logged-in user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# --- 2. Comment ViewSet ---
class CommentViewSet(viewsets.ModelViewSet):
    # We will only query comments related to a specific post in the URL
    queryset = Comment.objects.all() 
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    # Automatically set the author of the comment to the currently logged-in user
    def perform_create(self, serializer):
        # The Post ID will be passed in the request data, which the serializer handles.
        serializer.save(author=self.request.user)