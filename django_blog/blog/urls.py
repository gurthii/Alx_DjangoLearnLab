from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Blog posts (CRUD using class-based views)
    path('posts/', views.PostListView.as_view(), name='listing_post'),
    path('post/new/', views.PostCreateView.as_view(), name='creating_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='viewing_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='editing_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='deleting_post'),
    
    # Search and Tags
    path('search/', views.search_posts, name='search_posts'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
    
    # Comment URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
