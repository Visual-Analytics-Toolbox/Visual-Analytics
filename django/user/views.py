from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from . import schema


@schema.current_user_viewset_schema
class CurrentUserViewSet(viewsets.ViewSet):
    def list(self, request):
        serializer = UserInfoSerializer(request.user)
        print(request.user)
        return Response(serializer.data)


@schema.token_view_schema
class TokenView(APIView):
    def get(self, request):
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        return Response({"token": user_token.key}, 200)


@schema.refresh_token_view_schema
class RefreshToken(APIView):
    # this is required to allow non admin users to refresh their token
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        user_token.delete()
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        user_token.save()
        return Response({"token": user_token.key}, 201)
