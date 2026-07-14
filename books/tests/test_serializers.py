import pytest

from books.models import Book
from books.serializers import BookSerializer


@pytest.mark.django_db
def test_book_serializer_returns_expected_fields():
    book = Book.objects.create(
        title="Arquitetura Limpa",
        author="Robert C. Martin",
        published_year=2017,
        description="Livro sobre arquitetura de software.",
    )

    data = BookSerializer(book).data

    assert data["id"] == book.id
    assert data["title"] == "Arquitetura Limpa"
    assert data["author"] == "Robert C. Martin"
    assert data["published_year"] == 2017
    assert data["description"] == "Livro sobre arquitetura de software."
    assert "created_at" in data
    assert "updated_at" in data


def test_book_serializer_accepts_valid_data():
    serializer = BookSerializer(
        data={
            "title": "Django APIs",
            "author": "William S. Vincent",
            "published_year": 2024,
            "description": "Livro sobre APIs com Django.",
        }
    )

    assert serializer.is_valid()


def test_book_serializer_rejects_future_published_year():
    serializer = BookSerializer(
        data={
            "title": "Livro do Futuro",
            "author": "Autor Teste",
            "published_year": 2999,
            "description": "Ano invalido.",
        }
    )

    assert not serializer.is_valid()
    assert "published_year" in serializer.errors
