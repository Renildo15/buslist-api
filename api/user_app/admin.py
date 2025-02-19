from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import BusStop, DriverProfile, NumericToken, StudentProfile, User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    readonly_fields = ["password"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                    "is_student",
                    "is_driver",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(BusStop)
admin.site.register(DriverProfile)
admin.site.register(StudentProfile)
admin.site.register(NumericToken)
