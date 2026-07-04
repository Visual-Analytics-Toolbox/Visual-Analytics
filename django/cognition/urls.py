from . import views
from rest_framework import routers

representation_models = [
    "audiodata",
    "ballmodel",
    "ballcandidates",
    "ballcandidatestop",
    "cameramatrix",
    "cameramatrixtop",
    "odometrydata",
    "fieldpercept",
    "fieldpercepttop",
    "goalpercept",
    "goalpercepttop",
    "multiballpercept",
    "ransaccirclepercept2018",
    "ransaclinepercept",
    "robotinfo",
    "shortlinepercept",
    "scanlineedgelpercept",
    "scanlineedgelpercepttop",
    "teammessagedecision",
    "teamstate",
    "whistlepercept",
    "robotpose",
]

app_name = "cognition"

urlpatterns = []

router = routers.DefaultRouter()
router.register("cognitionframe", views.CognitionFrameViewSet)

for repr_model in representation_models:
    router.register(
        repr_model,
        views.DynamicModelViewSet,
        basename=repr_model,
    )

urlpatterns += router.urls
