from django.db import models
from pacientes.models import Paciente
from profesionales.models import Profesional

class HistorialClinico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    descripcion = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historial {self.id_historial} - Paciente: {self.paciente}"
