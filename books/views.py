from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer


def index(request):
    return JsonResponse(
        {
            "message": "Bookstore API",
            "books_url": "/api/books/",
        }
    )


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
