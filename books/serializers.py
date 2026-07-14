from django.utils import timezone
from rest_framework import serializers

from .models import Book, Category, Order, Product


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "published_year",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_published_year(self, value):
        current_year = timezone.now().year

        if value > current_year:
            raise serializers.ValidationError(
                "O ano de publicacao nao pode ser maior que o ano atual."
            )

        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_detail",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "category_detail", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "product_detail",
            "customer_name",
            "customer_email",
            "quantity",
            "status",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "product_detail",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")

        return value
