from django.apps import AppConfig

class AutenticacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autenticacion"

    def ready(self):
        # importa signals
        import autenticacion.signals
        #import autenticacion.authentication 
