from django.apps import AppConfig


class MyTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_platform'

    def ready(self):
        import my_platform.signals