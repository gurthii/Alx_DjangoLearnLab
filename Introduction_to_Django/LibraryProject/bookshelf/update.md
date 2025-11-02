## Start by importing the respective model from app
`from bookshelf.models import Book`

## To update, use the .update() method
```py
given_book = Book.objects.filter(title="1984")

given_book.update(title="Nineteen Eighty-Four")
```
## or update the .title value
```py
book = Book.object.get(title="1984")
book.title = "Nineteen Eighty-Four"
```