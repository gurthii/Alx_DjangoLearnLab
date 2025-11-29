from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book instances.
    Includes custom validation to prevent future publication years.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future ({value})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author instances,
    embedding a nested representation of all related books.
    """
    books = BookSerializer(many=True, read_only=True)  
    # "books" comes from related_name="books" on the Book model

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
