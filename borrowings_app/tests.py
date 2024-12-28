import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from books_app.serializers import BookSerializer
from books_app.tests import sample_book
from borrowings_app.models import Borrowing
from books_app.models import Book
from borrowings_app.serializers import BorrowingListSerializer, BorrowingSerializer, ReadBorrowingSerializer

BORROWING_LIST_URL = reverse("borrowings_app:borrowing-list")
BORROWING_DETAIL_URL = reverse("borrowings_app:borrowing-detail", kwargs={"pk": 1})


def get_first_user():
    return get_user_model().objects.first()


def sample_borrowing(**params) -> Borrowing:
    book_payload = {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "Joanne Rowling",
        "cover": "SOFT",
        "daily_fee": "2",
    }
    book_serializer = BookSerializer(data=book_payload)
    book = None
    if book_serializer.is_valid():
        book = book_serializer.save()
    user = get_first_user()
    now_date = now().date()
    expected_return_date = now_date + datetime.timedelta(days=1)
    payload = {
        "borrow_date": now().date(),
        "expected_return_date": expected_return_date,
        "actual_return_date": "",
        "book": book.id,
        "user": user.id,
    }
    payload.update(params)
    serializer = BorrowingSerializer(data=payload)
    if serializer.is_valid():
        return serializer.save()
    return serializer.errors


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_borrowing_list(self):
        sample_borrowing()
        borrowing = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowing, many=True)
        res = self.client.get(BORROWING_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_list_is_active_param(self):
        sample_borrowing()
        sample_borrowing()
        r_path = reverse(
            "borrowings_app:borrowing-borrowing-return",
            kwargs={"pk": 1}
        )
        res = self.client.post(path=r_path, data={},)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(
            reverse("borrowings_app:borrowing-list",),
            {"is_active": False}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        res = self.client.get(
            reverse("borrowings_app:borrowing-list", ),
            {"is_active": True}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertIsNone(res.data[0]["actual_return_date"])

    def test_create_borrowing_allowed_and_forbidden(self):
        book = sample_book()
        user = get_user_model().objects.first()
        now_date = now().date()
        expected_return_date = now_date + datetime.timedelta(days=1)
        payload = {
            "borrow_date": now_date,
            "expected_return_date": expected_return_date,
            "actual_return_date": "",
            "book": book.id,
            "user": user.id,
        }
        res = self.client.post(path=BORROWING_LIST_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(path=BORROWING_LIST_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("out_of_stock")[0],
            f"The book '{book.title}' is out of stock."
        )

        payload["borrow_date"] = now_date - datetime.timedelta(days=1)
        res = self.client.post(path=BORROWING_LIST_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("borrow_date")[0],
            f"Borrowing a book in the past is not allowed."
        )
        payload["borrow_date"] = now_date
        payload["expected_return_date"] = now_date - datetime.timedelta(days=1)
        res = self.client.post(path=BORROWING_LIST_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("expected_return_date")[0],
            f"The return date cannot be earlier than the borrow date."
        )

    def test_retrieve_borrowing(self):
        borrowing = sample_borrowing()
        res = self.client.get(path=BORROWING_DETAIL_URL)
        serializer = ReadBorrowingSerializer(borrowing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_return_borrowings(self):
        borrowing = sample_borrowing()
        book_inventory = 0
        book_inventory_after_return = 1
        book = Book.objects.first()
        self.assertEqual(book.inventory, book_inventory)
        r_path = reverse(
            "borrowings_app:borrowing-borrowing-return",
            kwargs={"pk": borrowing.id}
        )
        res = self.client.post(path=r_path, data={}, )
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book.inventory, book_inventory_after_return)

