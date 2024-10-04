from uuid import uuid4

from django.db import models


class InstitutionAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "institution_address"
        verbose_name = "Institution Address"
        verbose_name_plural = "Institution Addresses"

    def __str__(self):
        return self.address


# Create your models here.
class Institution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    acronym = models.CharField(max_length=10)
    address = models.OneToOneField(InstitutionAddress, on_delete=models.CASCADE)
    in_vacation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "institution"
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return f"{self.name} - {self.acronym}"
