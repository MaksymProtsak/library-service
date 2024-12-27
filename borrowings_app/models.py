from django.db import models
from django.conf import settings

from books_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @staticmethod
    def validate_borrow(attrs: dict) -> dict:
        errors = {}
        if attrs["book"].inventory == 0:
            errors["out_of_stock"] = (
                f"The book '{attrs["book"].title}' is out of stock."
            )
        return errors
