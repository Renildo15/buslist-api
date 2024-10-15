from django.urls import path

from .views import *

urlpatterns = [
    path("student/register/<str:matric>/", student_create_view, namespace="student_register"),
    path("student/info/", student_get_info_view, namespace="student_info"),
    path("student/<str:user_uuid>/profile/", student_profile_view, name="student_profile"),
    path("student/<str:user_uuid>/profile/update/", student_profile_update_view, name="student_profile_update"),
    path("whoami/", whoami_view),
]

urlpatternsstaff = [path("staff/list/users", staff_get_all_users_view, name="staff_list_users")]

urlpatterns += urlpatternsstaff
