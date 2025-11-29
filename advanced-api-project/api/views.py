from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
    Public (read-only) access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID.
    Public (read-only) access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
