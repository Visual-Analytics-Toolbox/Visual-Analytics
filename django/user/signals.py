from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from .roles import sync_roles

@receiver(pre_social_login)
def sync_keycloak_roles(request, sociallogin, **kwargs):
    if sociallogin.account.provider != 'keycloak':
        return
    
    extra_data = sociallogin.account.extra_data["userinfo"]
    roles = []

    if 'realm_access' in extra_data and 'roles' in extra_data['realm_access']:
        roles.extend(extra_data['realm_access']['roles'])

    user = sociallogin.user
    
    is_admin_in_keycloak = 'berlin_united_admin' in roles

    has_changed = False

    if is_admin_in_keycloak:
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            has_changed = True
    else:
        if user.is_staff or user.is_superuser:
            user.is_staff = False
            user.is_superuser = False
            has_changed = True
    
    user = sync_roles(user,roles)

    if has_changed and user.pk:
        user.save()