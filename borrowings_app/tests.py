import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from books_app.tests import sample_book
from borrowings_app.models import Borrowing
from books_app.models import Book
from borrowings_app.serializers import BorrowingListSerializer

AIRPLANE_URL = reverse("borrowings_app:borrowing-list")


def sample_borrowing(**params) -> Borrowing:
    book = sample_book()
    user = get_user_model().objects.first()
    defaults = {
        "borrow_date": datetime.date(year=2024, month=1, day=1),
        "expected_return_date": datetime.date(year=2024, month=1, day=2),
        "actual_return_date": None,
        "book": book,
        "user": user,
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airplane_list(self):
        sample_borrowing()
        borrowing = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowing, many=True)
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing_allowed(self):
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
        res = self.client.post(path=AIRPLANE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
