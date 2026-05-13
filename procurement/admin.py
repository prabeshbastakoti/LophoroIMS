from django.contrib import admin
from .models import Supplier, Purchase, PurchaseItem
from .services import receive_purchase


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "phone", "email")


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "created_by", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "supplier__name", "created_by__username")
    inlines = [PurchaseItemInline]

    actions = ["receive_selected_purchases"]

    def receive_selected_purchases(self, request, queryset):
        received = 0
        for purchase in queryset:
            try:
                receive_purchase(purchase)
                received += 1
            except Exception:
                pass
        self.message_user(request, f"Received {received} purchase(s).")

    receive_selected_purchases.short_description = "Receive selected purchases"