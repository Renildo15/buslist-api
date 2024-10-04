import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)
User = get_user_model()

USER_MODEL = "User"
DRIVER_PROFILE_MODEL = "Driver Profile"
STUDENT_PROFILE_MODEL = "Student Profile"
BUS_LIST_MODEL = "Bus List"
BUS_LIST_STUDENT_MODEL = "Bus List Student"
BUS_STOP_MODEL = "Bus Stop"
BUS_STOP_ADDRESS_MODEL = "Bus Stop Address"
NOTICE_MODEL = "Notice"
INSTITUTION_MODEL = "Institution"
INSTITUTION_ADRESS_MODEL = "Institution Address"

USERS = {"admin": ["Admin", "admin@admin.com", "admin123"]}

GROUPS = {
    "Admin": {
        #  "log entry": ["add", "delete", "change", "view"],
        # "group": ["add", "delete", "change", "view"],
        # "permission": ["add", "delete", "change", "view"],
        # "user": ["add", "delete", "change", "view", "activate"],
        # "content type": ["add", "delete", "change", "view"],
        # "session": ["add", "delete", "change", "view"],
        # Custom permissions
        USER_MODEL: ["add_user", "delete_user", "change_user", "view_user"],
        DRIVER_PROFILE_MODEL: [
            "add_driverprofile",
            "delete_driverprofile",
            "change_driverprofile",
            "view_driverprofile",
        ],
        STUDENT_PROFILE_MODEL: [
            "add_studentprofile",
            "delete_studentprofile",
            "change_studentprofile",
            "view_studentprofile",
        ],
        BUS_LIST_MODEL: [
            "add_buslist",
            "delete_buslist",
            "change_buslist",
            "view_buslist",
        ],
        BUS_LIST_STUDENT_MODEL: [
            "add_busliststudent",
            "delete_busliststudent",
            "change_busliststudent",
            "view_busliststudent",
        ],
        BUS_STOP_MODEL: [
            "add_busstop",
            "delete_busstop",
            "change_busstop",
            "view_busstop",
        ],
        BUS_STOP_ADDRESS_MODEL: ["add", "delete", "change", "view"],
        NOTICE_MODEL: ["add_notice", "delete_notice", "change_notice", "view_notice"],
        INSTITUTION_MODEL: [
            "add_institution",
            "delete_institution",
            "change_institution",
            "view_institution",
        ],
        INSTITUTION_ADRESS_MODEL: [
            "add_institutionaddress",
            "delete_institutionaddress",
            "change_institutionaddress",
            "view_institutionaddress",
        ],
    },
    "Student": {
        # Custom permissions
        USER_MODEL: ["add_user", "change_user", "view_user"],
        STUDENT_PROFILE_MODEL: [
            "add_studentprofile",
            "change_studentprofile",
            "view_studentprofile",
        ],
        BUS_LIST_MODEL: ["view_buslist"],
        BUS_STOP_MODEL: ["view_busstop"],
        BUS_STOP_ADDRESS_MODEL: ["view_busstopaddress"],
        NOTICE_MODEL: ["view_notice"],
        INSTITUTION_MODEL: ["view_institution"],
        INSTITUTION_ADRESS_MODEL: ["view_institutionaddress"],
    },
    "Driver": {
        # Custom permissions
        USER_MODEL: ["add_user", "change_user", "view_user"],
        DRIVER_PROFILE_MODEL: [
            "add_driverprofile",
            "change_driverprofile",
            "view_driverprofile",
        ],
        BUS_LIST_MODEL: [
            "add_buslist",
            "delete_buslist",
            "change_buslist",
            "view_buslist",
        ],
        BUS_STOP_MODEL: ["view_busstop"],
        BUS_STOP_ADDRESS_MODEL: ["view_busstopaddress"],
        NOTICE_MODEL: ["add_notice", "delete_notice", "change_notice", "view_notice"],
        INSTITUTION_MODEL: ["view_institution"],
        INSTITUTION_ADRESS_MODEL: ["view_institutionaddress"],
    },
}


class Command(BaseCommand):
    help = "Create default groups"

    def handle(self, *args, **kwargs):
        self.create_permissions()
        self.create_groups()

    def create_permissions(self):
        logger.info("Creating permissions")
        content_type = ContentType.objects.get_for_model(User)
        permission, created = Permission.objects.get_or_create(
            codename="activate_user",
            name="Can activate user",
            content_type=content_type,
        )

        created_str = "created" if created else "already exists"
        logger.info(f"Permission {permission} {created_str}")

    def create_groups(self):
        logger.info("Creating groups")
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)
            self.add_permission_to_group(group_name, new_group)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Group {group_name} created"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Group {group_name} already exists")
                )

    def add_permission_to_group(self, group_name, new_group):
        for app_model in GROUPS[group_name]:
            for permission_name in GROUPS[group_name][app_model]:
                name_sliced = permission_name.split("_")
                name = f"Can {name_sliced[0]} {app_model}"
                logger.info(f"Creating permission {name}")
                # breakpoint()
                try:
                    model_add_perm = Permission.objects.get(name=name)
                except Permission.DoesNotExist:
                    logger.error(f"Permission {name} does not exist")
                    continue

                new_group.permissions.add(model_add_perm)
