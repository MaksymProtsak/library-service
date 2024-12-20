from rest_framework import viewsets

from django.shortcuts import render

from borrowings_app.models import Borrowing
from borrowings_app.serializers import BorrowSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowSerializer
