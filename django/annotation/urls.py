from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
    path("annotation-count/", views.AnnotationCount.as_view(), name="annotation-count"),
    path("annotation-task/", views.AnnotationTask.as_view(), name="annotation-task"),
    path(
        "annotation-task/border",
        views.AnnotationTaskBorder.as_view(),
        name="annotation-task-border",
    ),
    path(
        "annotation-task/multiple",
        views.AnnotationTaskMultiple.as_view(),
        name="annotation-task-border",
    ),
    path("image-validation/",views.ImageValidationView.as_view(),name="validation-view")
]

router = routers.DefaultRouter()
router.register("annotations", views.AnnotationViewSet)

urlpatterns += router.urls
