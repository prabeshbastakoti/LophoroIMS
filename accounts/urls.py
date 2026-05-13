from django.urls import path
from .views import (
    login_view,
    logout_view,
    user_list,
    user_create,
    user_edit,
    user_delete,
    user_reset_password,
    audit_log_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("users/", user_list, name="user_list"),
    path("users/add/", user_create, name="user_create"),
    path("users/<int:user_id>/edit/", user_edit, name="user_edit"),
    path("users/<int:user_id>/delete/", user_delete, name="user_delete"),
    path("users/<int:user_id>/reset-password/", user_reset_password, name="user_reset_password"),
    path("audit-log/", audit_log_view, name="audit_log"),
]