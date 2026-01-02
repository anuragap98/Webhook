from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib import messages
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import guest_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .serializers import UserSerializer, RegistrationSerializer, ProfileSerializer

# -----------------------------------------------------------------------------
# TEMPLATE VIEWS
# -----------------------------------------------------------------------------


@login_required
def profile_view(request):
    """View to display the user's profile."""
    return render(request, "users/profile.html", {"user": request.user})


@login_required
def edit_profile(request):
    """View to update user and profile information."""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, "Success! Your profile details have been updated."
            )
            return redirect("users:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request, "users/edit_profile.html", {"u_form": u_form, "p_form": p_form}
    )


@login_required
def change_password(request):
    """View to handle password changes."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, "Security update: Your password has been changed."
            )
            return redirect("users:profile")
        messages.error(
            request, "Failed to update password. Please check the requirements."
        )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


@guest_required
def register_view(request):
    """Frontend registration for normal users."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to the platform, {user.username}!")
            return redirect("dashboard")
        messages.error(request, "Registration rejected. Please review your input.")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


@guest_required
def login_view(request):
    """Frontend login for normal users."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Note: RedirectStaffMiddleware will handle staff redirection globally.
            # We keep a check here for immediate feedback during the login process.
            if user.is_staff:
                messages.warning(
                    request, "Staff accounts must use the administrative portal."
                )
                return redirect("/admin/login/?next=/admin/")

            login(request, user)
            messages.info(request, f"Welcome back, {user.username}.")
            return redirect("dashboard")
        messages.error(request, "Access denied. Invalid credentials.")
    else:
        form = AuthenticationForm(request)
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """Standard logout view."""
    logout(request)
    messages.info(request, "Session ended. You have been logged out.")
    return redirect("users:login")


# -----------------------------------------------------------------------------
# API VIEWS
# -----------------------------------------------------------------------------


class RegisterAPIView(generics.CreateAPIView):
    """Endpoint for programmatic registration."""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    """Endpoint to get/update current user details."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """Endpoint to get/update profile-specific data."""

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class LoginAPIView(APIView):
    """Custom API Login logic."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                return Response(
                    {"detail": "Staff must authenticate via administrative endpoints."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(
            {"detail": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPIView(APIView):
    """Standard API Logout."""

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
