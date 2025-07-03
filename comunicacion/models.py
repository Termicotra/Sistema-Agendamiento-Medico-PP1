from django.db import models
from empleado.models import Empleado
from turno.models import Turno
from paciente.models import Paciente

class Anuncio(models.Model):
    class EstadoAnuncioChoices(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        NO_ACTIVO = 'No activo', 'No activo'

    id_anuncio = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=True, blank=True)
    titulo = models.CharField(null=False, blank=False, max_length=256)
    descripcion = models.TextField(blank=True, max_length=512)
    estado = models.CharField(
        choices=EstadoAnuncioChoices.choices,
        default=EstadoAnuncioChoices.ACTIVO
    )
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"Anuncio: {self.titulo} el {self.fecha} - Estado: {self.estado}"
    
class Notificacion(models.Model):
    class EstadoNotificacionChoices(models.TextChoices):
        ENVIADO = 'Enviado', 'Enviado'
        NO_ENVIADO = 'No Enviado', 'No Enviado'
    id_notificacion = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=True, blank=True)
    mensaje = models.TextField(null=False, blank=False, max_length=512)
    estado = models.CharField(
        choices=EstadoNotificacionChoices.choices,
        default=EstadoNotificacionChoices.ENVIADO
    )
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=False, blank=False, default=None)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return (f"Notificación del Paciente {self.paciente.nombre} {self.paciente.apellido} "
                f"con CI: {self.paciente.ci} el {self.fecha} "
                f"con Turno {self.turno.id_turno} - Estado: {self.estado}")
