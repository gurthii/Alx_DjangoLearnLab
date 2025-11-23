from  rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # This method dynamically sets permissions based on the action being performed
    def get_permissions(self):
        # Allow any authenticated user to list or retrieve books (GET requests)
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        # Restrict create, update, and destroy actions (POST, PUT, DELETE) to Admin users only
        else:
            permission_classes = [permissions.IsAdminUser]
            
        return [permission() for permission in permission_classes]