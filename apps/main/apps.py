from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
    verbose_name = 'Основной'

    def ready(self):
        import apps.main.signals
