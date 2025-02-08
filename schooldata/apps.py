from django.apps import AppConfig


class SchooldataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "schooldata"

    def ready(self):
        import schooldata.signals
