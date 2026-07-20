from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIRequestFactory

from books.models import Category, Order, Product
from books.views import CategoryViewSet, OrderViewSet, ProductViewSet


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="adilson",
        email="adilson@example.com",
        password="senha-teste",
    )


def token_header_for(user):
    token = Token.objects.create(user=user)

    return {"HTTP_AUTHORIZATION": f"Token {token.key}"}


@pytest.mark.django_db
def test_category_viewset_lists_categories(api_factory):
    Category.objects.create(name="Backend", description="Livros de backend.")
    view = CategoryViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/categories/")

    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Backend"


@pytest.mark.django_db
def test_category_viewset_creates_category(api_factory):
    view = CategoryViewSet.as_view({"post": "create"})
    request = api_factory.post(
        "/api/categories/",
        {
            "name": "Arquitetura",
            "description": "Livros sobre arquitetura de software.",
        },
        format="json",
    )

    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.filter(name="Arquitetura").exists()


@pytest.mark.django_db
def test_product_viewset_retrieves_product(api_factory):
    category = Category.objects.create(name="APIs")
    product = Product.objects.create(
        category=category,
        name="Django REST Framework",
        price=Decimal("89.90"),
        stock=8,
    )
    view = ProductViewSet.as_view({"get": "retrieve"})
    request = api_factory.get(f"/api/products/{product.pk}/")

    response = view(request, pk=product.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Django REST Framework"
    assert response.data["category_detail"]["name"] == "APIs"


@pytest.mark.django_db
def test_product_viewset_creates_product(api_factory):
    category = Category.objects.create(name="Python")
    view = ProductViewSet.as_view({"post": "create"})
    request = api_factory.post(
        "/api/products/",
        {
            "category": category.pk,
            "name": "Python Fluente",
            "description": "Livro de Python.",
            "price": "120.00",
            "stock": 4,
            "is_available": True,
        },
        format="json",
    )

    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.filter(name="Python Fluente", category=category).exists()


@pytest.mark.django_db
def test_order_viewset_rejects_unauthenticated_user(api_factory):
    view = OrderViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/orders/")

    response = view(request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_order_viewset_creates_order_for_authenticated_user(api_factory, user):
    category = Category.objects.create(name="Django")
    product = Product.objects.create(
        category=category,
        name="Django APIs",
        price=Decimal("50.00"),
        stock=3,
    )
    view = OrderViewSet.as_view({"post": "create"})
    request = api_factory.post(
        "/api/orders/",
        {
            "product": product.pk,
            "customer_name": "Adilson Henrique",
            "customer_email": "adilson@example.com",
            "quantity": 2,
        },
        format="json",
        **token_header_for(user),
    )

    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["user"] == user.pk
    assert response.data["total_price"] == "100.00"
    assert Order.objects.filter(
        customer_email="adilson@example.com",
        user=user,
    ).exists()


@pytest.mark.django_db
def test_order_viewset_lists_only_authenticated_user_orders(api_factory, user):
    other_user = User.objects.create_user(
        username="outro-usuario",
        email="outro@example.com",
        password="senha-teste",
    )
    category = Category.objects.create(name="Seguranca")
    product = Product.objects.create(
        category=category,
        name="Livro de Seguranca",
        price=Decimal("80.00"),
        stock=5,
    )
    Order.objects.create(
        product=product,
        user=user,
        customer_name="Adilson Henrique",
        customer_email="adilson@example.com",
        quantity=1,
    )
    Order.objects.create(
        product=product,
        user=other_user,
        customer_name="Outro Cliente",
        customer_email="outro@example.com",
        quantity=1,
    )
    view = OrderViewSet.as_view({"get": "list"})
    request = api_factory.get("/api/orders/", **token_header_for(user))

    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["customer_email"] == "adilson@example.com"


@pytest.mark.django_db
def test_order_viewset_rejects_invalid_quantity(api_factory, user):
    category = Category.objects.create(name="Testes")
    product = Product.objects.create(
        category=category,
        name="Livro de Testes",
        price=Decimal("75.00"),
        stock=2,
    )
    view = OrderViewSet.as_view({"post": "create"})
    request = api_factory.post(
        "/api/orders/",
        {
            "product": product.pk,
            "customer_name": "Cliente Teste",
            "customer_email": "cliente@example.com",
            "quantity": 0,
        },
        format="json",
        **token_header_for(user),
    )

    response = view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "quantity" in response.data
