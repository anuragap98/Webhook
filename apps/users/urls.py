from django.urls import path
from .views import (
    profile_view,
    edit_profile,
    change_password,
    register_view,
    login_view,
    logout_view,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserDetailAPIView,
    ProfileAPIView,
)

app_name = "users"

urlpatterns = [
    # Template Views
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/password/", change_password, name="change_password"),
    # API Views
    path("api/register/", RegisterAPIView.as_view(), name="api_register"),
    path("api/login/", LoginAPIView.as_view(), name="api_login"),
    path("api/logout/", LogoutAPIView.as_view(), name="api_logout"),
    path("api/me/", UserDetailAPIView.as_view(), name="api_me"),
    path("api/me/profile/", ProfileAPIView.as_view(), name="api_profile"),
]
