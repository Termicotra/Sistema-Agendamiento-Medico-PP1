from django.db import models
from profesionales.models import Profesional
from pacientes.models import Paciente
from secretarios.models import Secretario

class Turno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    estado = models.TextField()
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    secretario = models.ForeignKey(Secretario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Turno {self.id_turno} - {self.fecha} {self.hora}"
