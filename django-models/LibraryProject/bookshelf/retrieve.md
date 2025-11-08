## Start by importing the respective model from app
`from bookshelf.models import Book`

# To retrieve all created objects(books)

```py
# Use the objects.get() method
my_book = Book.objects.get(title="1984")

print(my_book.title, my_book.author, my_book.publication_year)

# Returns all object instances as a QuerySet; iterable using a for loop and respective attributes such as .title, .author
```