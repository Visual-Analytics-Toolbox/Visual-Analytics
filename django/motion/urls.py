from . import views
from rest_framework import routers

app_name = "motion"

representation_models = [
    "imudata",
    "fsrdata",
    "buttondata",
    "sensorjointdata",
    "accelerometerdata",
    "inertialsensordata",
    "motionstatus",
    "motorjointdata",
    "gyrometerdata",
]

urlpatterns = []

router = routers.DefaultRouter()
router.register("motionframe", views.MotionFrameViewSet)

for repr_model in representation_models:
    router.register(repr_model, views.DynamicModelViewSet, basename=repr_model)

urlpatterns += router.urls
