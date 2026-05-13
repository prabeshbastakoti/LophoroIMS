from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),
    path("catalog/", include("catalog.urls")),
    path("inventory/", include("inventory.urls")),
    path("orders/", include("orders.urls")),
    path("procurement/", include("procurement.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)