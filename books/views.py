from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from .models import Book, Category, Order, Product
from .serializers import (
    BookSerializer,
    CategorySerializer,
    OrderSerializer,
    ProductSerializer,
)


def index(request):
    return JsonResponse(
        {
            "message": "Bookstore API",
            "books_url": "/api/books/",
            "categories_url": "/api/categories/",
            "products_url": "/api/products/",
            "orders_url": "/api/orders/",
        }
    )


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("product", "product__category")
    serializer_class = OrderSerializer
