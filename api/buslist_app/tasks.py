from celery import shared_task
from django.utils import timezone

from .models import BusList


@shared_task
def disable_expired_buslist():
    now = timezone.now()
    expired_buslist = BusList.objects.filter(list_time_final__lt=now, is_enable=True)
    expired_buslist.update(is_enable=False)
