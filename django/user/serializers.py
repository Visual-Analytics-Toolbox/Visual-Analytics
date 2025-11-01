from rest_framework import serializers
from .models import VATUser
from .permission import IsBerlinUnited


class VATUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VATUser
        fields = "__all__"

class UserInfoSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = VATUser
        fields = ["username","is_admin"]

    def get_is_admin(self,obj):
        request = self.context.get('request')

        if not request:
            return False
        
        admin_class = IsBerlinUnited()
        return admin_class.has_permission(request, None)