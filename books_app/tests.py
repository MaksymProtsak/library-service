from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from books_app.models import Book
from books_app.serializers import BookListSerializer

from decimal import Decimal

BOOK_URL = reverse("books_app:book-list")


def sample_airplane(**params) -> Book:
    defaults = {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "Joanne Rowling",
        "cover": "SOFT",
        "daily_fee": "1",
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

    def test_create_book_forbidden(self):
        payload = {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "Joanne Rowling",
            "cover": "Soft",
            "daily_fee": "1",
        }
        res = self.client.post(path=BOOK_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        book_inventory = 1
        payload = {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "Joanne Rowling",
            "cover": "SOFT",
            "daily_fee": "2",
        }
        res = self.client.post(path=BOOK_URL, data=payload)
        book = Book.objects.get(id=res.data["id"])
        book_title = payload["title"]
        book_author = payload["author"]
        book_cover = payload["cover"].lower().capitalize()
        book_daily_fee = Decimal(
            payload['daily_fee']
        ).quantize(Decimal('1.00'))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertEqual(book.cover, payload["cover"])
        self.assertEqual(book.daily_fee, Decimal(payload["daily_fee"]))
        self.assertEqual(book.inventory, book_inventory)
        self.assertEqual(
            str(book),
            f"{book_title} "
            f"by {book_author} "
            f"({book_cover}) - "
            f"${book_daily_fee}/day "
            f"(in stock: {book_inventory})"
        )
