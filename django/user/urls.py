from django.urls import path
from .views import LoginView, LogoutView,DummyView

urlpatterns = [
    path("login", LoginView, name="mylogin"),
    path("logout", LogoutView, name="mylogout"),
    path("signup", DummyView, name="signup"),
]
