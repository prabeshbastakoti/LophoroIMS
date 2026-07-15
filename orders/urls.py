from django.urls import path
from .views import (
    order_list, order_create, order_edit, order_detail, order_confirm_view,
    order_cancel_view, order_return_view, bill_view, invoice_download_view,
    customer_list, customer_create, customer_edit, customer_search_api,
)

urlpatterns = [
    path("", order_list, name="order_list"),
    path("add/", order_create, name="order_create"),
    path("<int:order_id>/", order_detail, name="order_detail"),
    path("<int:order_id>/edit/", order_edit, name="order_edit"),
    path("<int:order_id>/confirm/", order_confirm_view, name="order_confirm"),
    path("<int:order_id>/cancel/", order_cancel_view, name="order_cancel"),
    path("<int:order_id>/return/", order_return_view, name="order_return"),
    path("<int:order_id>/bill/", bill_view, name="order_bill"),
    path("invoices/<int:invoice_id>/pdf/", invoice_download_view, name="invoice_pdf"),
    path("customers/", customer_list, name="customer_list"),
    path("customers/add/", customer_create, name="customer_create"),
    path("customers/search/", customer_search_api, name="customer_search_api"),
    path("customers/<int:customer_id>/edit/", customer_edit, name="customer_edit"),
]