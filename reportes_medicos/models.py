from django.db import models
from historiales_clinicos.models import HistorialClinico

class ReporteMedico(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    detalle = models.TextField()
    historial = models.ForeignKey(HistorialClinico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha}"
