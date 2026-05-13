from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import User, AuditLog
from .forms import UserCreateForm, UserUpdateForm, PasswordResetForm


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/")
        if request.user.role != "ADMIN":
            return HttpResponseForbidden("Access denied. Only admin can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/analytics/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role != role:
                messages.error(request, "You selected the wrong login role.")
                return render(request, "accounts/login.html")

            login(request, user)
            return redirect("/analytics/")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


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
            form.save()
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

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
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
def user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        if user_obj == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect("/accounts/users/")
        user_obj.delete()
        messages.success(request, f"User '{user_obj.username}' has been deleted.")
        return redirect("/accounts/users/")
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