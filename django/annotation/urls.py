from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
    path("annotation-count/", views.AnnotationCount.as_view(), name="annotation-count"),
]

router = routers.DefaultRouter()
router.register("annotations", views.AnnotationViewSet)
router.register("validation", views.ValidationViewSet)

urlpatterns += router.urls
