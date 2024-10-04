from django.contrib import admin

from .models import BusList, BusListStudent, Notice

# Register your models here.
admin.site.register(BusList)
admin.site.register(BusListStudent)
admin.site.register(Notice)
