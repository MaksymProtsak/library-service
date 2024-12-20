from rest_framework import serializers

from borrowings_app.models import Borrowing


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book_id",
            "user_id",
        )
