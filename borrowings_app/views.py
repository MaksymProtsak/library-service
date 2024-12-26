from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from books_app.models import Book
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingSerializer,
    ReadBorrowingSerializer,
    BorrowingListSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ReadBorrowingSerializer
        elif self.action == "list":
            return BorrowingListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        book = instance.book
        count = Book.objects.filter(title=book.title).count()
        Book.objects.filter(title=book.title).update(inventory=count)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrowing.objects.all()

        return Borrowing.objects.filter(user=self.request.user)
