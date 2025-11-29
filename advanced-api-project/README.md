# API View Structure

The project uses Django REST Framework generic views to handle CRUD operations
for the Book model:

- GET /api/books/ → ListView (public)
- GET /api/books/<id>/ → DetailView (public)
- POST /api/books/create/ → CreateView (authenticated)
- PUT /api/books/<id>/update/ → UpdateView (authenticated)
- DELETE /api/books/<id>/delete/ → DestroyView (authenticated)

Permissions:
- AllowAny for read operations.
- IsAuthenticated for create, update, delete operations.

All serializers perform validation, including custom rules such as enforcing valid publication years.

# Query Features (Filtering, Searching, Ordering)

The BookListView supports:

### Filtering
- /api/books/?title=1984
- /api/books/?publication_year=1949
- /api/books/?author=1

### Searching
- /api/books/?search=orwell
- /api/books/?search=animal

### Ordering
- /api/books/?ordering=title
- /api/books/?ordering=-publication_year

The filtering is powered by django-filter,
while searching and ordering use DRF’s SearchFilter and OrderingFilter.
