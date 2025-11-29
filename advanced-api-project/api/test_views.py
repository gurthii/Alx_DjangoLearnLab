from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user and login credentials
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create an author and some books
        self.author = Author.objects.create(name="Test Author")
        self.book1 = Book.objects.create(title="Test Book 1", publication_year=2000, author=self.author)
        self.book2 = Book.objects.create(title="Another Book", publication_year=2010, author=self.author)

        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    def login(self):
        login_successful = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_successful, "Login failed in test setup")

    def test_list_books_public(self):
        # Anyone can GET list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_detail_book_public(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_requires_auth(self):
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id,
        }

        # Unauthenticated should fail
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login user and retry
        self.login()
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_update_book_requires_auth(self):
        update_data = {"title": "Updated Title", "publication_year": 2005, "author": self.author.id}

        # Unauthenticated should fail
        response = self.client.put(self.update_url(self.book1.id), update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login and update
        self.login()
        response = self.client.put(self.update_url(self.book1.id), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_book_requires_auth(self):
        # Unauthenticated fails
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login and delete
        self.login()
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filtering(self):
        response = self.client.get(self.list_url, {"title": "Test Book 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Book 1")

    def test_searching(self):
        response = self.client.get(self.list_url, {"search": "Another"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Another Book")

    def test_ordering(self):
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item["publication_year"] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
