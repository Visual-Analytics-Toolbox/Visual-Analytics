from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import VATUser, Organization
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.admin import SocialAccountAdmin as BaseSocialAccountAdmin

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(Group)
admin.site.unregister(SocialAccount)


class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("organization",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("organization",)}),
    )

    # Optionally, display organization in the list view
    list_display = BaseUserAdmin.list_display + ("organization",)


@admin.register(SocialAccount)
class SocialAccountAdmin(BaseSocialAccountAdmin, ModelAdmin):
    pass


admin.site.register(VATUser, CustomUserAdmin)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Organization)
class CustomAdminClass(ModelAdmin):
    pass
