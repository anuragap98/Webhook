from django.shortcuts import render


def profile_view(request):
    # Simple example view that renders user profile
    return render(request, "users/profile.html", {})
