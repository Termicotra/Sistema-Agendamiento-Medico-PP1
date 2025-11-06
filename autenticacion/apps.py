from django.apps import AppConfig

class AutenticacionConfig(AppConfig):
    name = "autenticacion"

    def ready(self):
        # importa signals
        import autenticacion.signals
