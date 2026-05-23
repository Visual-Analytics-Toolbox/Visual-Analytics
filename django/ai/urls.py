from django.urls import path
from . import views

app_name = "ai"

urlpatterns = [
    path("ai/rl/train", views.MattermostGitLabTriggerView.as_view(), name="rl"),
]
