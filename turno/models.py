from django.db import models
from profesional.models import Profesional
from paciente.models import Paciente
from empleado.models import Empleado

class Turno(models.Model):
    class EstadoTurnoChoices(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        NO_ACTIVO = 'No activo', 'No activo'
        CANCELADO = 'Cancelado', 'Cancelado'

    class ModalidadTurnoChoices(models.TextChoices):
        PRESENCIAL = 'Presencial', 'Presencial'
        VIRTUAL = 'Virtual', 'Virtual'

    id_turno = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    modalidad = models.CharField(
        choices=ModalidadTurnoChoices.choices,
        default=ModalidadTurnoChoices.PRESENCIAL
    )
    estado = models.CharField(
        choices=EstadoTurnoChoices.choices,
        default=EstadoTurnoChoices.ACTIVO
    )
    motivo = models.TextField(null=False, blank=False, max_length=128)
    fue_notificado = models.BooleanField(null=False, blank=False)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return (f"Turno de Paciente {self.paciente.nombre} {self.paciente.apellido} con CI: {self.paciente.ci} "
                f"el {self.fecha} a las {self.hora}"
                f" con el Profesional {self.profesional.nombre} {self.profesional.apellido} con CI: {self.profesional.ci} con Especialidad {self.profesional.especialidad} "
                f"- Estado: {self.estado}")
