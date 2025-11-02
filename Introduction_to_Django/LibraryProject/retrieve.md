## Start by importing the respective model from app
`from bookshelf.models import Book`

# To retrieve all created objects(books)

```py
# Use the objects.all() method
all_books = Book.objects.all()

for book in all_books:
    print(book.title, book.author, book.publication_year)

# Returns all object instances as a QuerySet; iterable using a for loop and respective attributes such as .title, .author
```