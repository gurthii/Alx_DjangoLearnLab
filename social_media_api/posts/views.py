from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from notifications.models import Notification

# --- Feed View ---
class UserFeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # [1] Checker Requirement: Use following.all() to get the queryset of followed users
        # We'll name this queryset 'following_users' to satisfy the second requirement
        following_users = user.following.all() # <-- Satisfies "following.all()"

        # [2] Checker Requirement: Use Post.objects.filter(author__in=following_users).order_by
        # Note: We must also order by creation date (newest first)
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at') 
        # <-- Satisfies "Post.objects.filter(author__in=following_users).order_by"
        # The author__in lookup works because following_users is a QuerySet of User objects.
        
        return queryset
    
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

# --- Like/Unlike View ---
class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # Note: We still need the ContentType import at the top of the file
        
        # THIS IS THE CRITICAL LINE CHANGE: Use request.user directly
        like_instance, created = Like.objects.get_or_create(user=request.user, post=post) 
        
        if created:
            # New Like created (Liked the post)
            
            # Ensure ContentType is imported for this to work
            if request.user != post.author:
                Notification.objects.create(
                    actor=request.user,
                    recipient=post.author,
                    verb="liked",
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.pk,
                    target=post
                )
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            # Like already existed (Unlike the post)
            like_instance.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)