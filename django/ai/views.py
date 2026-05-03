from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
import hashlib
import hmac
import time
import os


class SlackGitLabTriggerView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 1. Verify Slack Signature (Same as before)
        if not self._is_valid_slack_request(request):
            return Response(status=status.HTTP_403_FORBIDDEN)

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

    def _is_valid_slack_request(self, request):
        secret_str = os.environ.get("SLACK_SIGNING_SECRET", "")

        # 2. CONVERT TO BYTES (This fixes your TypeError)
        secret_bytes = secret_str.encode("utf-8")
        timestamp = request.META.get("HTTP_X_SLACK_REQUEST_TIMESTAMP", "")
        signature = request.META.get("HTTP_X_SLACK_SIGNATURE", "")

        # Check for replay attacks
        if abs(time.time() - int(timestamp)) > 60 * 5:
            return False

        # IMPORTANT: Use request.body for the raw string, NOT request.data
        sig_basestring = f"v0:{timestamp}:".encode() + request.body
        my_sig = (
            "v0=" + hmac.new(secret_bytes, sig_basestring, hashlib.sha256).hexdigest()
        )

        return hmac.compare_digest(my_sig, signature)
