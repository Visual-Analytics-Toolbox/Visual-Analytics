from django.urls import path
from . import views
from rest_framework import routers

app_name = "image"

urlpatterns = [
    path("image-count/", views.ImageCountView.as_view(), name="image-count"),
    path("image/update/", views.ImageUpdateView.as_view(), name="image-update"),
    path("image-sync/", views.SynchronizedImage.as_view(), name="image-sync"),
]

router = routers.DefaultRouter()
router.register("images", views.ImageViewSet)

urlpatterns += router.urls
