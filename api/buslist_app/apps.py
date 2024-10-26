from django.apps import AppConfig


class BuslistAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.buslist_app"

    def ready(self):
        import api.buslist_app.signals
