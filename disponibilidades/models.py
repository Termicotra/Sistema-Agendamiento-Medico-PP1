from django.db import models
from profesionales.models import Profesional

class Disponibilidad(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    dia = models.TextField()
    hora_inicio = models.TextField()
    hora_fin = models.TextField()
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesional} - {self.dia} ({self.hora_inicio}-{self.hora_fin})"
