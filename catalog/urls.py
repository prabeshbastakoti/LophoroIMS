from django.urls import path
from .views import (
    category_list,
    category_create,
    category_edit,
    category_toggle_active,
    category_delete,
    product_list,
    product_create,
    product_edit,
    product_toggle_active,
    product_delete,
    search,
)

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("categories/add/", category_create, name="category_create"),
    path("categories/<int:category_id>/edit/", category_edit, name="category_edit"),
    path("categories/<int:category_id>/toggle-active/", category_toggle_active, name="category_toggle_active"),
    path("categories/<int:category_id>/delete/", category_delete, name="category_delete"),
    path("products/", product_list, name="product_list"),
    path("products/add/", product_create, name="product_create"),
    path("products/<int:product_id>/edit/", product_edit, name="product_edit"),
    path("products/<int:product_id>/toggle-active/", product_toggle_active, name="product_toggle_active"),
    path("products/<int:product_id>/delete/", product_delete, name="product_delete"),
    path("search/", search, name="search"),
]
