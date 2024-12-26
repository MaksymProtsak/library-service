from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        books = Book.objects.filter(title=validated_data["book"].title)
        book_inventory = books.first().inventory
        if book_inventory:
            books.update(inventory=book_inventory - 1)
            return Borrowing.objects.create(**validated_data)
        raise ValueError("Book not found")

    def validate(self, attrs):
        data = super(BorrowSerializer, self).validate(attrs=attrs)
        errors = Borrowing.validate_borrow(attrs)
        if errors:
            raise ValidationError(errors)
        return data


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class ReadBorrowSerializer(BorrowSerializer):
    book = BookSerializer(read_only=True)
    user = PartialUserSerializer(read_only=True,)

    class Meta(BorrowSerializer.Meta):
        fields = BorrowSerializer.Meta.fields + ("user",)


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta(BorrowSerializer.Meta):
        fields = BorrowSerializer.Meta.fields + ("actual_return_date",)