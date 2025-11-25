from django.contrib import admin
from django.urls import path

from users.views import (
    RegisterView,
    LoginView,
    CookieTokenRefreshView,
    LogoutView,
    ProtectedView,
)

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/protected/", ProtectedView.as_view(), name="protected"),
]
