from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
    path(
        "video/annotation/<int:pk>",
        views.VideoAnnotation.as_view(),
        name="video-annotation",
    ),
    path(
        "situations/gc/audio/",
        views.RawGCSituationAudioUpload.as_view(),
        name="raw-gc-audio",
    ),
]

router = routers.DefaultRouter()
router.register("situations/gc", views.RawGCSituationViewSet)

urlpatterns += router.urls
