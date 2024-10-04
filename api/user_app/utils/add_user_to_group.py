from django.contrib.auth.models import Group


def add_user_to_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.add(group)
    user.save()
