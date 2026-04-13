from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
     path("video/annotation/<int:pk>",views.VideoAnnotation.as_view(),name="video-annotation")
]

router = routers.DefaultRouter()


urlpatterns += router.urls
