from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import schema
import requests
import os


@schema.mattermost_gitlab_trigger_view_schema
class MattermostGitLabTriggerView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Token "):
            return Response(
                {"text": "Missing or invalid authorization header."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Split "Token <value>" to isolate the actual token string
        try:
            incoming_token = auth_header.split(" ")[1]
        except IndexError:
            return Response(
                {"text": "Malformed authorization header."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if incoming_token != os.environ.get("MATTERMOST_TOKEN", ""):
            return Response(
                {"text": "Unauthorized token."}, status=status.HTTP_403_FORBIDDEN
            )

        # 2. Extract Data
        # Slack sends data as 'application/x-www-form-urlencoded'
        commit_sha = request.data.get("text", "").strip()

        if not commit_sha:
            return Response({"text": "⚠️ Please provide a commit SHA or branch name."})

        # 3. Call GitLab API via Requests
        try:
            project_id = os.environ.get("GITLAB_RL_PROJECT_ID")
            trigger_token = os.environ.get("GITLAB_RL_TRIGGER_TOKEN")

            payload = {"token": trigger_token, "ref": commit_sha}

            gl_response = requests.post(
                f"https://scm.cms.hu-berlin.de/api/v4/projects/{project_id}/trigger/pipeline",
                data=payload,
                timeout=5,  # Don't hang the request
            )

            if gl_response.status_code == 201:
                pipeline_url = gl_response.json().get("web_url")
                return Response(
                    {
                        "response_type": "in_channel",
                        "text": f"🚀 *Pipeline Triggered!*\n*Ref:* `{commit_sha}`\n*Link:* {pipeline_url}",
                    }
                )
            else:
                return Response({"text": f"❌ GitLab API Error: {gl_response.text}"})

        except requests.exceptions.RequestException as e:
            return Response({"text": f"💥 Connection Error: {str(e)}"})
