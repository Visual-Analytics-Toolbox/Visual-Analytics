from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TokenView(APIView):
    def get(self, request):
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        return Response({"token": user_token.key}, 200)


class RefreshToken(APIView):
    # this is required to allow non admin users to refresh their token
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        user_token.delete()
        user_token, created = Token.objects.get_or_create(user=self.request.user)
        user_token.save()
        return Response({"token": user_token.key}, 201)
