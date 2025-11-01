from django.urls import path
from .views import LoginView, LogoutView,DummyView,CurrentUserViewSet
from rest_framework import routers

urlpatterns = [
    path("login", LoginView, name="mylogin"),
    path("logout", LogoutView, name="mylogout"),
    path("signup", DummyView, name="signup"),
]

router = routers.DefaultRouter()
router.register("user",CurrentUserViewSet)
urlpatterns += router.urls