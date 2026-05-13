from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseForbidden
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


# Restrict admin panel access
class AdminSiteRestriction(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == "ADMIN"


admin.site.__class__ = AdminSiteRestriction