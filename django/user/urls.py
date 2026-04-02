from django.urls import path
from django.views.generic import RedirectView
from .views import (
    LoginView,
    LogoutView,
    DummyView,
    CurrentUserViewSet,
    TokenView,
    RefreshToken,
)
from rest_framework import routers

urlpatterns = [
    path("", RedirectView.as_view(url="/events")),
    path("login", LoginView, name="mylogin"),
    path("logout", LogoutView, name="mylogout"),
    path("signup", DummyView, name="signup"),
    path("token", TokenView.as_view(), name="token"),
    path("token/refresh", RefreshToken.as_view(), name="refresh_token"),
]

router = routers.DefaultRouter()
router.register("user", CurrentUserViewSet)
urlpatterns += router.urls
