from django.apps import AppConfig

class CampusconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campusConnect'

    def ready(self):
        # Ensures signals.py is loaded when the app is ready
        import campusConnect.signals
