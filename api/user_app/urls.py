from django.urls import path

from .views import *

urlpatterns = [
    path("student/register/", student_create_view),
    path("student/info/", student_get_info_view),
    path("student/<str:user_uuid>/profile/", student_profile_view),
    path("student/<str:user_uuid>/profile/update/", student_profile_update_view),
]

urlpatternsstaff = [path("staff/list/users", staff_get_all_users_view)]

urlpatterns += urlpatternsstaff
