from django.db import models
from django.conf import settings
from django.utils.timezone import now

from books_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @staticmethod
    def validate_borrow(attrs: dict) -> dict:
        now_date = now().date()
        errors = {}
        borrow_date = attrs["borrow_date"]
        expected_return_date = attrs["expected_return_date"]

        if attrs["book"].inventory == 0:
            errors["out_of_stock"] = (
                f"The book '{attrs["book"].title}' is out of stock."
            )
        if now_date > borrow_date:
            errors["borrow_date"] = "Borrowing a book in the past is not allowed."
        if not (borrow_date < expected_return_date):
            errors["expected_return_date"] = "The return date cannot be earlier than the borrow date."

        return errors
