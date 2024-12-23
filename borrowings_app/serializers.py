from django.contrib.auth import get_user_model
from rest_framework import serializers

from books_app.models import Book
from books_app.serializers import BookSerializer
from borrowings_app.models import Borrowing


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def create(self, validated_data):
        count = Book.objects.filter(title=validated_data["book"].title).count()
        book_inventory = Book.objects.filter(title=validated_data["book"].inventory)
        if book_inventory:
            Book.objects.filter(title=validated_data["book"].title).update(inventory=count - 1)
            return Borrowing.objects.create(**validated_data)
        raise ValueError("Book not found") # Need to use validate method from Borrowing model


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class ReadBorrowSerializer(BorrowSerializer):
    book = BookSerializer(read_only=True)
    user = PartialUserSerializer(read_only=True,)
