from django.urls import path
from . import views

app_name = "ai"

urlpatterns = [
    path("ai/rl-trigger", views.SlackGitLabTriggerView.as_view(), name="rl-trigger"),
    path("ai/rl/train", views.MattermostGitLabTriggerView.as_view(), name="rl"),
]
