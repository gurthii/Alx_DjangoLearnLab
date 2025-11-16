from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# Query 2: All books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Query 3: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    return librarian


# Example usage (only works in Django shell or after setup)
if __name__ == "__main__":
    print("Books by Author:")
    for book in get_books_by_author("J.K. Rowling"):
        print(book.title)

    print("\nBooks in Library:")
    for book in get_books_in_library("City Library"):
        print(book.title)

    print("\nLibrarian for Library:")
    print(get_librarian_for_library("City Library").name)
