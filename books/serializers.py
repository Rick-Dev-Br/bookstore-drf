from django.utils import timezone
from rest_framework import serializers

from .models import Book


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
