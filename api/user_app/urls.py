from django.urls import path

from .views import *

urlpatterns = [
    path("student/register/<str:matric>/", student_create_view),
    path("student/info/", student_get_info_view),
    path("student/<str:user_uuid>/profile/update/", student_profile_update_view),
    path("student/profile/create/", user_student_create_profile_view),
    path("whoami/", whoami_view),
    path("change-password/<str:user_uuid>/", change_password_view),
    path("forgot-password/", reset_password_view),
    path("avatar/upload/", avatar_upload_view),
    path(
        "reset-password/<str:uidb64>/<str:token>/", reset_password_confirm_view
    ),
    path("check-numeric-token/", check_numeric_token),
]

urlpatternsstaff = [path("staff/list/users", staff_get_all_users_view)]

urlpatterns += urlpatternsstaff
