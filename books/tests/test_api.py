import pytest
from django.urls import reverse

from books.models import Book


def test_index_returns_api_summary(client):
    response = client.get(reverse("index"))

    assert response.status_code == 200
    assert response.json()["books_url"] == "/api/books/"


@pytest.mark.django_db
def test_books_api_lists_books(client):
    Book.objects.create(
        title="Clean Code",
        author="Robert C. Martin",
        published_year=2008,
    )

    response = client.get("/api/books/")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Clean Code"
