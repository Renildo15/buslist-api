from django.urls import path

from .views import *

urlpatterns = [
    path("student/<str:matric_number>/register/", student_view),
    path("student/<str:user_uuid>/profile/", student_profile_view),
    path("student/<str:user_uuid>/profile/update/", student_profile_update_view),
]
