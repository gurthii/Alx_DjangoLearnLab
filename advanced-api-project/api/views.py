from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
    Retrieves all books with advanced query capabilities.

    Features:
    - Filtering: filter by title, publication_year, and author.
    - Searching: search text in title or author's name.
    - Ordering: order results by title, publication_year, or id.

    Examples:
        /api/books/?title=1984
        /api/books/?publication_year=1949
        /api/books/?author=1
        /api/books/?search=orwell
        /api/books/?ordering=title
        /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering fields
    filterset_fields = ["title", "publication_year", "author"]

    # Searching fields
    search_fields = ["title", "author__name"]

    # Ordering fields
    ordering_fields = ["title", "publication_year", "id"]

    # Default ordering if none is provided
    ordering = ["id"]
