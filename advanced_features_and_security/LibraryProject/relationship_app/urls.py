from django.urls import path
from .views import list_books
import views 
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book,
)

urlpatterns = [
    # Book and library views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views using built-in auth views with templates
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Role-based views
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # Secured book management views
    path('book/add/', views.add_book, name='add_book/'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book/'),
    path('book/<int:pk>/delete/', delete_book, name='delete_book'),
]
