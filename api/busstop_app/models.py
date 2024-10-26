from uuid import uuid4

from django.db import models


class BusStopAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    neighborhood = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=8)

    class Meta:
        db_table = "bus_stop_address"
        verbose_name = "Bus Stop Address"
        verbose_name_plural = "Bus Stop Addresses"

    def __str__(self):
        return self.address


# Create your models here.
class BusStop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.OneToOneField(BusStopAddress, on_delete=models.CASCADE)

    class Meta:
        db_table = "bus_stop"
        verbose_name = "Bus Stop"
        verbose_name_plural = "Bus Stops"

    def __str__(self):
        return self.name
