from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from books_app.models import Book
from books_app.serializers import BookListSerializer

BOOK_URL = reverse("books_app:book-list")


def sample_airplane(**params) -> Book:
    defaults = {
            "title": "HHarry Potter and the Philosopher's Stone",
            "author": "Joanne Rowling",
            "cover": "SOFT",
            "daily_fee": "1",
            "inventory": "5",
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        sample_airplane()
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
