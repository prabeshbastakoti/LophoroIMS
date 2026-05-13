from django.contrib import admin
from .models import Order, OrderItem
from .services import confirm_order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "created_by__username")
    inlines = [OrderItemInline]

    actions = ["confirm_selected_orders"]

    def confirm_selected_orders(self, request, queryset):
        confirmed = 0
        for order in queryset:
            try:
                confirm_order(order)
                confirmed += 1
            except Exception:
                # skip orders that cannot be confirmed
                pass
        self.message_user(request, f"Confirmed {confirmed} order(s).")

    confirm_selected_orders.short_description = "Confirm selected orders"