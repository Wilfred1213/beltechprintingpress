from django.apps import AppConfig


class BeltechappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beltechApp'

    def ready(self):
        import beltechApp.signals