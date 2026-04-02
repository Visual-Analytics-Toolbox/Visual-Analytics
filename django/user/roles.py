from django.contrib.auth.models import Group, Permission


def sync_roles(user, roles):
    if (
        "berlin_united_readonly" in roles
        and not user.groups.filter(name="berlin_united_readonly").exists()
    ):
        group, group_created = Group.objects.get_or_create(
            name="berlin_united_readonly"
        )

        if group_created:
            # FIXME we maybe want diffrent permissions here
            view_permissions = Permission.objects.filter(codename__startswith="view_")

            group.permissions.set(view_permissions)

        user.groups.add(group)

    elif (
        "berlin_united_readonly" not in roles
        and user.groups.filter(name="berlin_united_readonly").exists()
    ):
        group = Group.objects.get(name="berlin_united_readonly")
        user.groups.remove(group)

    return user
