from django.contrib import admin

from .models import Institution, InstitutionAddress

# Register your models here.
admin.site.register(Institution)
admin.site.register(InstitutionAddress)
