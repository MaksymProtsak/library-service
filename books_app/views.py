from rest_framework import viewsets

from django.shortcuts import render

from books_app.models import Book
from books_app.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
