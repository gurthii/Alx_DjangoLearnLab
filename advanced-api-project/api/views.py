from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

"""
View Layer Overview
-------------------

This module defines all API endpoints related to the Book model using Django REST Framework's
generic views. These generic classes dramatically reduce boilerplate by providing built-in
implementations for common operations like listing, retrieving, creating, updating,
and deleting database records.

View Responsibilities:
- BookListView: Public read-only access to all books.
- BookDetailView: Public read-only access to a single book.
- BookCreateView: Allows authenticated users to create new books.
- BookUpdateView: Allows authenticated users to update existing books.
- BookDeleteView: Allows authenticated users to delete books.

Customization:
- perform_create and perform_update hooks allow injection of custom logic without rewriting
  request handling.
- Permission classes restrict write actions while keeping read operations open.
"""


class BookListView(generics.ListAPIView):
    """
    Retrieves all books.
    Public endpoint: no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by its ID.
    Public endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book entry.
    Restricted to authenticated users.
    Custom validation happens in BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Hook that runs after validation.
        Could be extended with:
        - assigning request.user
        - additional custom logic
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book entry.
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook for custom update behavior.
        Extend this if you need extra logic.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes an existing book.
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
