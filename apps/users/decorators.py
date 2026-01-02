from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def normal_user_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is NOT staff,
    redirecting staff users to the admin panel.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        if request.user.is_staff:
            messages.info(request, "Staff members are redirected to the admin panel.")
            return redirect("/admin/")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def guest_required(view_func):
    """
    Decorator for views that checks that the user is NOT logged in.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect("/admin/")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
