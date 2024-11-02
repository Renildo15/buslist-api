from uuid import uuid4

from django.db import models

from api.user_app.models import User


# Create your models here.
class BusList(models.Model):
    SHIFT_CHOICES = (
        ("M", "MATUTINO"),
        ("V", "VESPERTINO"),
        ("N", "NOTURNO"),
    )
    TYPE_CREATION_CHOICES = (
        ("MANUAL", "MANUAL"),
        ("AUTOMATICO", "AUTOMÁTICO"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    list_date = models.DateField()
    list_time_initial = models.DateTimeField()
    list_time_final = models.DateTimeField()
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES)
    type_creation = models.CharField(max_length=10, choices=TYPE_CREATION_CHOICES)
    students = models.ManyToManyField(
        User, related_name="bus_lists", through="BusListStudent"
    )
    is_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bus_list"
        verbose_name = "Bus List"
        verbose_name_plural = "Bus Lists"

    def __str__(self):
        formatted_date = self.list_date.strftime("%d/%m/%Y")
        return f"{self.name} - {formatted_date}"


class BusListStudent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    bus_list = models.ForeignKey(BusList, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    end_class_time = models.TimeField()
    is_return = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bus_list_student"
        verbose_name = "Bus List Student"
        verbose_name_plural = "Bus List Students"

    def __str__(self):
        return f"{self.bus_list.name} - {self.student.username}"


class Notice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    viewed = models.BooleanField(default=False)
    buslist = models.ForeignKey(BusList, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "notice"
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def __str__(self):
        return self.title
