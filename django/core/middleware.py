from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Token "):
            token_key = auth_header.split(" ")[1]
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                request.user = AnonymousUser()
        return self.get_response(request)


class AllauthStatusMiddleware:
    # https://docs.allauth.org/en/latest/headless/openapi-specification/#section/Authentication-Flows
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if this is the specific allauth session endpoint
        if request.path.endswith('/_allauth/browser/v1/auth/session'):
            # If allauth returned 401, change it to 200
            if response.status_code == 401:
                response.status_code = 200
        
        return response