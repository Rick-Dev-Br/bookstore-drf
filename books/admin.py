from django.contrib import admin

from .models import Book, Category, Order, Product


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_year", "created_at")
    search_fields = ("title", "author")
    list_filter = ("published_year",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "product", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email", "product__name")
    readonly_fields = ("created_at", "updated_at")
