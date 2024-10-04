import json
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from api.institution_app.models import Institution, InstitutionAddress

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "data", "institutions.json")

        try:
            with open(file_path, "r") as f:
                institutions = json.load(f)

                for institution in institutions:
                    if not Institution.objects.filter(
                        acronym=institution["acronym"]
                    ).exists():
                        logger.info(f"Creating institution {institution['acronym']}")
                        address = InstitutionAddress.objects.create(
                            address=institution["address"],
                            city=institution["city"],
                            state=institution["state"],
                            zip_code=institution["zip_code"],
                        )

                        Institution.objects.create(
                            name=institution["name"],
                            phone_number=institution["phone_number"],
                            acronym=institution["acronym"],
                            address=address,
                        )
                        logger.info(f"Institution {institution['acronym']} created")
                    else:
                        logger.info(
                            f"Institution {institution['acronym']} already exists"
                        )
        except Exception as e:
            logger.error(f"Error creating institutions: {e}")
            raise e
