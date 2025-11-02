## Start by importing the respective model from app
`from bookshelf.models import Book`

## To update
```py
given_book = Book.objects.filter(title="1984")

given_book.update(title="Nineteen Eighty-Four")
```