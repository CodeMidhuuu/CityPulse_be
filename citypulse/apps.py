from django.apps import AppConfig

class CitypulseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citypulse'

    def ready(self):
        import citypulse.signals  # Import the signals file here to ensure the signals are registered
