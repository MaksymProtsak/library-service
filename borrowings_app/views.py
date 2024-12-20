from rest_framework import viewsets
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet

from django.shortcuts import render

from borrowings_app.models import Borrowing
from borrowings_app.serializers import BorrowSerializer, ReadBorrowSerializer


class BorrowViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ReadBorrowSerializer
        return self.serializer_class
