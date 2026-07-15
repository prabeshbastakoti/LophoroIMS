from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .audit import log_action
from .decorators import admin_required
from .models import User, AuditLog
from .forms import UserCreateForm, UserUpdateForm, PasswordResetForm, AdminRegisterForm
from .utils import is_last_active_admin


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/analytics/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        cache_key = f"login_attempts:{username}"
        attempts = cache.get(cache_key, 0)

        if attempts >= settings.LOGIN_ATTEMPT_LIMIT:
            messages.error(
                request,
                "Too many failed login attempts. Please try again in 15 minutes."
            )
            return render(request, "accounts/login.html", {
                "no_users_exist": not User.objects.exists()
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role != role:
                messages.error(request, "You selected the wrong login role.")
                return render(request, "accounts/login.html", {
                    "no_users_exist": not User.objects.exists()
                })

            cache.delete(cache_key)
            login(request, user)
            return redirect("/analytics/")
        else:
            cache.set(cache_key, attempts + 1, timeout=settings.LOGIN_LOCKOUT_SECONDS)
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html", {
        "no_users_exist": not User.objects.exists()
    })


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def register_view(request):
    """Lets a brand-new deployment create its first Admin account without
    developer intervention. Locks itself once any user exists so ongoing
    user management stays through the Admin-only Manage Users panel."""
    if User.objects.exists():
        messages.error(request, "Setup already complete. Please sign in, or ask an admin to add your account.")
        return redirect("/accounts/login/")

    if request.method == "POST":
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Admin account created. Welcome to Lophoro IMS.")
            return redirect("/analytics/")
    else:
        form = AdminRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
@admin_required
def user_list(request):
    users = User.objects.all().order_by("username")
    return render(request, "accounts/user_list.html", {
        "users": users
    })


@login_required
@admin_required
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(request.user, "CREATE", user)
            return redirect("/accounts/users/")
    else:
        form = UserCreateForm()

    return render(request, "accounts/user_form.html", {
        "form": form,
        "page_title": "Add User",
        "mode": "create"
    })


@login_required
@admin_required
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    # Capture pre-edit state before the ModelForm mutates user_obj in place during validation.
    was_last_active_admin = is_last_active_admin(user_obj)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            demoting = form.cleaned_data["role"] != "ADMIN"
            deactivating = not form.cleaned_data["is_active"]
            if was_last_active_admin and (demoting or deactivating):
                messages.error(
                    request,
                    "You can't remove the last remaining Administrator. Promote another user to Admin first."
                )
            else:
                form.save()
                log_action(request.user, "UPDATE", user_obj)
                return redirect("/accounts/users/")
    else:
        form = UserUpdateForm(instance=user_obj)

    return render(request, "accounts/user_form.html", {
        "form": form,
        "page_title": f"Edit User: {user_obj.username}",
        "mode": "edit",
        "user_obj": user_obj
    })


@login_required
@admin_required
@require_POST
def user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj == request.user:
        messages.error(request, "You cannot delete your own account.")
    elif is_last_active_admin(user_obj):
        messages.error(
            request,
            "You can't remove the last remaining Administrator. Promote another user to Admin first."
        )
    else:
        deleted_pk = user_obj.pk
        try:
            user_obj.delete()
        except ProtectedError:
            messages.error(
                request,
                f"Cannot delete '{user_obj.username}' — they have created orders or purchases on record. "
                "Deactivate their account instead."
            )
        else:
            user_obj.pk = deleted_pk
            log_action(request.user, "DELETE", user_obj)
            messages.success(request, f"User '{user_obj.username}' has been deleted.")
    return redirect("/accounts/users/")


@login_required
@admin_required
def user_reset_password(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            user_obj.set_password(new_password)
            user_obj.save()
            log_action(request.user, "UPDATE", user_obj, "Password reset")
            return redirect("/accounts/users/")
    else:
        form = PasswordResetForm()

    return render(request, "accounts/password_reset_form.html", {
        "form": form,
        "user_obj": user_obj
    })


@login_required
@admin_required
def audit_log_view(request):
    logs = AuditLog.objects.select_related("user").order_by("-timestamp")[:500]
    return render(request, "accounts/audit_log.html", {"logs": logs})
