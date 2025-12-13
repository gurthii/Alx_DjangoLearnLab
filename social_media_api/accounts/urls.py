from django.urls import path
from .views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    # Registration endpoint (/api/auth/register)
    path('register/', RegisterView.as_view(), name='register'),
    
    # Login endpoint (/api/auth/login)
    path('login/', LoginView.as_view(), name='login'),
    
    # User profile management endpoint (/api/auth/profile)
    path('profile/', UserProfileView.as_view(), name='profile'),
]