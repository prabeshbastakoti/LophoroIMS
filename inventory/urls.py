from django.urls import path
from .views import stock_movement_list, current_stock

urlpatterns = [
    path("", current_stock, name="current_stock"),
    path("movements/", stock_movement_list, name="stock_movement_list"),
]
