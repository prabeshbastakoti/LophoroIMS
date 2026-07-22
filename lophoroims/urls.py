from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


def root_redirect(request):
    return redirect("/accounts/login/")


urlpatterns = [
    path("", root_redirect, name="root_redirect"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),
    path("catalog/", include("catalog.urls")),
    path("inventory/", include("inventory.urls")),
    path("orders/", include("orders.urls")),
    path("procurement/", include("procurement.urls")),
]

# Uploaded media. On cPanel/Passenger the app directory sits outside the web
# root, so Apache cannot serve MEDIA_ROOT itself and Django has to. Static
# files are handled by WhiteNoise, not here.
urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]