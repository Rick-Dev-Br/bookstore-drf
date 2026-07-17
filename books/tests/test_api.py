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
    data = response.json()
    assert data["count"] == 1
    assert data["next"] is None
    assert data["previous"] is None
    assert data["results"][0]["title"] == "Clean Code"


@pytest.mark.django_db
def test_books_api_limits_results_to_page_size(client):
    for index in range(6):
        Book.objects.create(
            title=f"Livro {index}",
            author="Autor Teste",
            published_year=2020,
        )

    response = client.get("/api/books/")

    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 6
    assert data["next"] is not None
    assert data["previous"] is None
    assert len(data["results"]) == 5
