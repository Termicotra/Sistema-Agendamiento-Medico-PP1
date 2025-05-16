from django.db import models
from Profesional.models import Profesional
from Paciente.models import Paciente
from Empleado.models import Empleado

class Turno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.DateTimeField(null=False, blank=False)
    modalidad = models.TextField(null=False, blank=False, max_length=128)
    estado = models.TextField(null=False, blank=False, max_length=128)
    motivo = models.TextField(null=False, blank=False, max_length=128)
    recordatorio = models.BooleanField(null=False, blank=False)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Turno {self.id_turno} - {self.fecha} {self.hora}"
