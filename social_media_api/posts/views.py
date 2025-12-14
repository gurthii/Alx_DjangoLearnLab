from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # Import the new permission class
# posts/views.py (Add to the existing file)

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

# --- Feed View ---
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 1. Get the current logged-in user
        user = self.request.user
        
        # 2. Get the IDs of all users the current user is following
        # The 'following' ManyToMany field is used here.
        followed_users_ids = user.following.values_list('id', flat=True)

        # 3. Filter the Post queryset to only include posts whose author ID 
        # is in the list of followed users' IDs.
        queryset = Post.objects.filter(author__id__in=followed_users_ids)
        
        # 4. Order the posts by creation date (newest first, already done in Model Meta, but good practice here)
        return queryset.order_by('-created_at')
    
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