from django.urls import path
from .views import (
    category_list,
    category_create,
    category_edit,
    product_list,
    product_create,
    product_edit,
    search,
)

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    path("categories/add/", category_create, name="category_create"),
    path("categories/<int:category_id>/edit/", category_edit, name="category_edit"),
    path("products/", product_list, name="product_list"),
    path("products/add/", product_create, name="product_create"),
    path("products/<int:product_id>/edit/", product_edit, name="product_edit"),
    path("search/", search, name="search"),
]