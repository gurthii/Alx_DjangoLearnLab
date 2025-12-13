from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer

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