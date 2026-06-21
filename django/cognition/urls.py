from django.urls import path
from . import views
from rest_framework import routers

app_name = "cognition"

urlpatterns = [
    path(
        "cognitionframe/update/",
        views.CognitionFrameUpdate.as_view(),
        name="cognitionframe-update",
    ),
]

router = routers.DefaultRouter()
router.register("cognitionframe", views.CognitionFrameViewSet)
router.register(
    "cognition/(?P<model_name>[^/.]+)",
    views.DynamicModelViewSet,
    basename="dynamicmodel",
)
router.register("log-first-frame", views.LogFirstFrame)

urlpatterns += router.urls
