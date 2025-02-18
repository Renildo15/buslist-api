from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    if sender.name == "api.buslist_app":  # Verifique se o sinal é para o seu app
        # Crie ou recupere um intervalo de 1 hora
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )

        # Crie ou recupere a tarefa periódica
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Desabilitar listas de ônibus expiradas',
            task='api.buslist_app.tasks.disable_expired_buslist',
        )
