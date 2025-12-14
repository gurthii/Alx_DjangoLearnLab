# accounts/urls.py

from django.urls import path
# Make sure you import ALL the views you use:
from .views import (
    RegisterView, 
    LoginView, 
    UserProfileView, 
    FollowUserView,  
    UnfollowUserView 
) 

urlpatterns = [
    # ... existing routes ...
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # NEW FOLLOW ROUTES
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]