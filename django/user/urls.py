from django.urls import path
from .views import (
    CurrentUserViewSet,
    TokenView,
    RefreshToken,
)
from rest_framework import routers

urlpatterns = [
    path("token", TokenView.as_view(), name="token"),
    path("token/refresh", RefreshToken.as_view(), name="refresh_token"),
]

router = routers.DefaultRouter()
router.register("user", CurrentUserViewSet)
urlpatterns += router.urls
