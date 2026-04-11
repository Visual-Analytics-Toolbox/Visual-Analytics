from django.urls import path
from . import views
from rest_framework import routers

app_name = "annotation"

urlpatterns = [
    
]

router = routers.DefaultRouter()


urlpatterns += router.urls
