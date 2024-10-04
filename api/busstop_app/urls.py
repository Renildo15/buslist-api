from django.urls import path

from .views import *

urlpatterns = [
    path("bus-stop-list/", bus_stop_list_view),
    path("bus-stop-create/", bus_stop_create_view),
]
