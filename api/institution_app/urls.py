from django.urls import path

from .views import institution_list_create

urlpatterns = [path("institutions/", institution_list_create)]
