from django.urls import path
from .views import (
    supplier_list,
    supplier_create,
    supplier_toggle_active,
    supplier_price_history,
    purchase_list,
    purchase_create,
    purchase_detail,
    purchase_receive_view,
)

urlpatterns = [
    path("suppliers/", supplier_list, name="supplier_list"),
    path("suppliers/add/", supplier_create, name="supplier_create"),
    path("suppliers/<int:supplier_id>/toggle-active/", supplier_toggle_active, name="supplier_toggle_active"),
    path("suppliers/<int:supplier_id>/price-history/", supplier_price_history, name="supplier_price_history"),
    path("purchases/", purchase_list, name="purchase_list"),
    path("purchases/add/", purchase_create, name="purchase_create"),
    path("purchases/<int:purchase_id>/", purchase_detail, name="purchase_detail"),
    path("purchases/<int:purchase_id>/receive/", purchase_receive_view, name="purchase_receive"),
]