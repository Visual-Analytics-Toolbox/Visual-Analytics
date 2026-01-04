from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from .roles import sync_roles
from django.db.models.signals import post_delete
from allauth.socialaccount.models import SocialAccount


@receiver(pre_social_login)
def sync_keycloak_roles(request, sociallogin, **kwargs):
    if sociallogin.account.provider != "keycloak":
        return

    extra_data = sociallogin.account.extra_data["userinfo"]
    roles = []

    if "realm_access" in extra_data and "roles" in extra_data["realm_access"]:
        roles.extend(extra_data["realm_access"]["roles"])

    user = sociallogin.user

    is_admin_in_keycloak = "admin" in extra_data["group"]

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

    if user.pk:
        # User already exists in DB (Returning User)
        # We can sync roles immediately
        sync_roles(user, roles)
    else:
        # New User (No ID yet)
        # We must wait until after allauth saves them to the DB
        pass

    if has_changed and user.pk:
        user.save()


@receiver(post_delete, sender=SocialAccount)
def delete_user_on_social_account_delete(sender, instance, **kwargs):
    user = instance.user

    if user is None:
        return

    # in case we add any other sso login methods later we don't want to delete the user after one social account got deleted
    if SocialAccount.objects.filter(user=user).exists():
        return

    if user.has_usable_password():
        return

    user.delete()
