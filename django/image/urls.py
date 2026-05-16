from . import views
from rest_framework import routers

app_name = "image"

urlpatterns = []

router = routers.DefaultRouter()
router.register("images", views.ImageViewSet)

urlpatterns += router.urls
