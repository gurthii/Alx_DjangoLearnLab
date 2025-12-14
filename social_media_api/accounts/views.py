from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

# Assuming these are from your project, keep them
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer

# Other imports you might have (e.g., from .models, .serializers)
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()

# 1. Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # The serializer instance now contains the 'token' field
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 2. Login View (Token Retrieval)
class LoginView(APIView):
    # Allow any user (authenticated or not) to access the login endpoint
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # User is authenticated, get or create token
            token, created = Token.objects.get_or_create(user=user)
            # The key deliverable: return the token
            return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# 3. User Profile View
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # Require authentication to access profile
    permission_classes = (permissions.IsAuthenticated,) 

    def get_object(self):
        # The object is the currently logged-in user
        return self.request.user
    
# --- Follow/Unfollow Base View ---
class FollowToggleView(generics.GenericAPIView): 
    permission_classes = [IsAuthenticated]

    # The logic remains the same, as GenericAPIView allows defining methods like post()
    def post(self, request, user_id):
        # 1. Get the target user to follow/unfollow
        target_user = get_object_or_404(User, id=user_id)
        current_user = request.user

        # 2. Check if the current user is trying to follow themselves
        if current_user == target_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Determine action based on the request path/logic (we'll make this a toggle)
        is_following = current_user.following.filter(id=target_user.id).exists()
        
        if self.is_follow_action:
            if not is_following:
                current_user.following.add(target_user)
                return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": f"You already follow {target_user.username}."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if is_following:
                current_user.following.remove(target_user)
                return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": f"You are not following {target_user.username}."}, status=status.HTTP_400_BAD_REQUEST)

# --- Concrete Follow View ---
class FollowUserView(FollowToggleView):
    is_follow_action = True

# --- Concrete Unfollow View ---
class UnfollowUserView(FollowToggleView):
    is_follow_action = False