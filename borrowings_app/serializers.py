from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books_app.models import Book
from books_app.serializers import BookSerializer
from borrowings_app.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
        )

    def create(self, validated_data):
        books = Book.objects.filter(title=validated_data["book"].title)
        book_inventory = books.first().inventory
        if book_inventory:
            books.update(inventory=book_inventory - 1)
            return Borrowing.objects.create(**validated_data)
        raise ValueError("Book not found")

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        errors = Borrowing.validate_borrow(attrs)
        if errors:
            raise ValidationError(errors)
        return data


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class ReadBorrowingSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = PartialUserSerializer(read_only=True, )

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + (
            "actual_return_date",
            "user",
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + (
            "actual_return_date",
            "user",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id",)

    def update(self, instance, validated_data):
        if instance.actual_return_date:
            raise ValidationError({"errors": "The book already returned."})
        instance.actual_return_date = now().date()
        instance.save()
        book = Book.objects.get(id=instance.book_id)
        Book.objects.filter(title=book.title).update(
            inventory=book.inventory + 1
        )
        return instance
