from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CategoryViewSet, OrderViewSet, ProductViewSet


router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
