from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingSerializer,
    ReadBorrowingSerializer,
    BorrowingListSerializer, BorrowingReturnSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
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
        elif self.action == "borrowing_return":
            return BorrowingReturnSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrowing.objects.all()

        return Borrowing.objects.filter(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        permission_classes=[IsAuthenticated],
    )
    def borrowing_return(self, request, pk=None):
        """
        Endpoint for return book.
        For borrowing instance, updated filed actual_return_date.
        For book, inventory for all books with same title rose +1.
        """
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
