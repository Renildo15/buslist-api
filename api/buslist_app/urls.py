from django.urls import path

from .views import *

urlpatterns = [
    path("list/enable/", bus_list_enable_list_view),
    path("list/enable/<uuid:bus_list_id>/", bus_list_enable_disable_view),
    path("list/", bus_list_get_all_view),
    path("create/", bus_list_create_view),
    path(
        "student/create/<uuid:bus_list_id>/<uuid:student_id>/",
        bus_list_student_create_view,
    ),
    path(
        "student/remove/<uuid:bus_list_id>/<uuid:student_id>/",
        bus_list_remove_student_view,
    ),
    path("notice/<uuid:bus_list_id>/", notice_create_list_view),
]
