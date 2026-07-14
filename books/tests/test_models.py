from decimal import Decimal

import pytest

from books.models import Category, Order, Product


@pytest.mark.django_db
def test_category_model_returns_name():
    category = Category.objects.create(
        name="Programacao",
        description="Livros sobre desenvolvimento de software.",
    )

    assert str(category) == "Programacao"


@pytest.mark.django_db
def test_product_model_keeps_category_and_returns_name():
    category = Category.objects.create(name="Backend")
    product = Product.objects.create(
        category=category,
        name="Django REST Framework",
        price=Decimal("89.90"),
        stock=12,
    )

    assert str(product) == "Django REST Framework"
    assert product.category == category
    assert product.price == Decimal("89.90")
    assert product.stock == 12
    assert product.is_available is True


@pytest.mark.django_db
def test_order_model_calculates_total_price_and_default_status():
    category = Category.objects.create(name="APIs")
    product = Product.objects.create(
        category=category,
        name="Livro de APIs",
        price=Decimal("50.00"),
        stock=5,
    )
    order = Order.objects.create(
        product=product,
        customer_name="Adilson Henrique",
        customer_email="adilson@example.com",
        quantity=3,
    )

    assert str(order) == f"Pedido #{order.pk} - Adilson Henrique"
    assert order.status == Order.Status.PENDING
    assert order.total_price == Decimal("150.00")
