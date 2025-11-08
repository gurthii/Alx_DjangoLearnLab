## Start by importing the respective model from app
`from bookshelf.models import Book`

## Create a Book instance and add a new book to the bookshelf

```py
create_book = Book(title="1984", author="George Orwell", publication_year=1949)
create_book.save()
```

## or, use the create method

```py
create_book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```
