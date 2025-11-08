## Start by importing the respective model from app
`from bookshelf.models import Book`

## To delete the book created and confirm deletion by trying to retrieve it
```py
select_book = Book.objects.get(title="Nineteen Eighty-Four")
select_book.delete()

all_books = Book.objects.all()
for book in all_books:
    print(book.title, book.author, book.publication_year)
```