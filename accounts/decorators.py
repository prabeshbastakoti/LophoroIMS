from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/")
        if request.user.role != "ADMIN":
            return HttpResponseForbidden("Access denied. Only admin can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
