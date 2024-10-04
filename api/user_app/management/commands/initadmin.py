import logging

from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = config("DJANGO_SUPERUSER_USERNAME", "admin@admin.com")
        password = config("DJANGO_SUPERUSER_PASSWORD", default="password")

        if not User.objects.filter(username=username).exists():
            logger.info(f"Creating admin user {username}")
            User.objects.create_superuser(username=username, password=password)
            logger.info(f"Admin user {username} created")
        else:
            logger.info(f"Admin user {username} already exists")
