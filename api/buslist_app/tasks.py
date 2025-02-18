from celery import shared_task
from .models import BusList
from django.utils import timezone

@shared_task
def disable_expired_buslist():
    now = timezone.now()
    expired_buslist = BusList.objects.filter(list_time_final__lt=now, is_enable=True)
    expired_buslist.update(is_enable=False)


