from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework.authtoken.models import Token

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
      
        user = super().save_user(request, sociallogin, form)

        extra_data = sociallogin.account.extra_data["userinfo"]
        roles = []

        if 'realm_access' in extra_data and 'roles' in extra_data['realm_access']:
            roles.extend(extra_data['realm_access']['roles'])
        
        if "berlin_united_admin_readonly" in roles:
           
            group, group_created = Group.objects.get_or_create(name="berlin_united_admin_readonly")

            if group_created:
                #FIXME we maybe want diffrent permissions here
                view_permissions = Permission.objects.filter(codename__startswith='view_')

                group.permissions.set(view_permissions)

            user.groups.add(group)

        Token.objects.create(user=user)

        return user