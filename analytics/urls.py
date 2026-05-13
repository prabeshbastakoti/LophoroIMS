from django.urls import path
from .views import (
    dashboard, eoq_report, abc_report, sales_trend_report,
    export_inventory_excel, export_inventory_pdf,
    export_orders_excel, export_orders_pdf,
    export_purchases_excel, export_purchases_pdf,
    export_customers_excel, export_customers_pdf,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("eoq/", eoq_report, name="eoq_report"),
    path("abc/", abc_report, name="abc_report"),
    path("trends/", sales_trend_report, name="sales_trend_report"),
    path("export/inventory/excel/", export_inventory_excel, name="export_inventory_excel"),
    path("export/inventory/pdf/", export_inventory_pdf, name="export_inventory_pdf"),
    path("export/orders/excel/", export_orders_excel, name="export_orders_excel"),
    path("export/orders/pdf/", export_orders_pdf, name="export_orders_pdf"),
    path("export/purchases/excel/", export_purchases_excel, name="export_purchases_excel"),
    path("export/purchases/pdf/", export_purchases_pdf, name="export_purchases_pdf"),
    path("export/customers/excel/", export_customers_excel, name="export_customers_excel"),
    path("export/customers/pdf/", export_customers_pdf, name="export_customers_pdf"),
]