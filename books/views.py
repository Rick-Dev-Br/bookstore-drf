from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").order_by("id")
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related("product", "product__category").filter(
            user=self.request.user
        ).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
