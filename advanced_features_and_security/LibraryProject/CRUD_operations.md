```py
# CREATE
create_book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# output: <Book: Book object (1)>

# RETRIEVE
all_books = Book.objects.all()

for book in all_books:
    print(book.title, book.author, book.publication_year)
# output: Nineteen Eighty-Four George Orwell 1949


# UPDATE
given_book = Book.objects.filter(title="1984")

given_book.update(title="Nineteen Eighty-Four")
# output: 1

# DELETE
select_book = Book.objects.get(title="Nineteen Eighty-Four")
select_book.delete()
# output: (1, {'bookshelf.Book': 1})
 
all_books = Book.objects.all()
for book in all_books:
    print(book.title, book.author, book.publication_year)
# output: 
```