from django.apps import AppConfig

from backend.scheduler import create_scheduler


scheduler = None


class SchedulerCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scheduler_core"

    def ready(self) -> None:
        global scheduler
        if scheduler is None:
            scheduler = create_scheduler()


