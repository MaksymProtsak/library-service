from django.contrib.auth import get_user_model
from rest_framework import serializers

from books_app.serializers import BookSerializer
from borrowings_app.models import Borrowing
from user.serializers import UserSerializer


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
        )


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class ReadBorrowSerializer(BorrowSerializer):
    book = BookSerializer(read_only=True)
    user = PartialUserSerializer(read_only=True,)
