from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.authtoken.models import Token
from .roles import sync_roles

class KeyCloakRoleGroupAdapter(DefaultSocialAccountAdapter):
    """maps keycloak roles to django groups on user creation"""
    def save_user(self, request, sociallogin, form=None):
      
        user = super().save_user(request, sociallogin, form)

        extra_data = sociallogin.account.extra_data["userinfo"]
        roles = []

        if 'realm_access' in extra_data and 'roles' in extra_data['realm_access']:
            roles.extend(extra_data['realm_access']['roles'])
        
        user = sync_roles(user,roles)

        Token.objects.create(user=user)

        return user