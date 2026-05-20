from . import views
from rest_framework import routers

app_name = "motion"

urlpatterns = []

router = routers.DefaultRouter()
router.register("motionframe", views.MotionFrameViewSet)
router.register(
    "motion/(?P<model_name>[^/.]+)",
    views.DynamicModelViewSet,
    basename="dynamicmodel",
)

urlpatterns += router.urls
