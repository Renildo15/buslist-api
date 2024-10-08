# Generated by Django 5.1.1 on 2024-10-04 21:53

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusStopAddress",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("address", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=2)),
                ("zip_code", models.CharField(max_length=8)),
            ],
            options={
                "verbose_name": "Bus Stop Address",
                "verbose_name_plural": "Bus Stop Addresses",
                "db_table": "bus_stop_address",
            },
        ),
        migrations.CreateModel(
            name="BusStop",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="busstop_app.busstopaddress",
                    ),
                ),
            ],
            options={
                "verbose_name": "Bus Stop",
                "verbose_name_plural": "Bus Stops",
                "db_table": "bus_stop",
            },
        ),
    ]
