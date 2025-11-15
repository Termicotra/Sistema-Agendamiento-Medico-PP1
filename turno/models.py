from django.db import models
from django.core.exceptions import ValidationError
from profesional.models import Profesional, Disponibilidad
from paciente.models import Paciente
from empleado.models import Empleado

class Turno(models.Model):
    class EstadoTurnoChoices(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        ACTIVO = 'Activo', 'Activo'
        COMPLETADO = 'Completado', 'Completado'
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
        default=EstadoTurnoChoices.PENDIENTE
    )
    motivo = models.TextField(null=False, blank=False, max_length=128)
    fue_notificado = models.BooleanField(null=False, blank=False)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return (f"{self.paciente.nombre} {self.paciente.apellido} {self.paciente.ci} "
                f"{self.profesional.especialidad} {self.fecha}")
    
    def clean(self):
        """Validar que la fecha y hora del turno coincidan con la disponibilidad del profesional."""
        super().clean()
        
        if not self.profesional or not self.fecha or not self.hora:
            return
        
        # Obtener el día de la semana en español
        dias_semana = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miercoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sabado',
            6: 'Domingo'
        }
        
        dia_turno = dias_semana.get(self.fecha.weekday())
        
        # Buscar disponibilidad del profesional para ese día
        disponibilidades = Disponibilidad.objects.filter(
            profesional=self.profesional,
            dia=dia_turno,
            esta_disponible=True
        )
        
        if not disponibilidades.exists():
            raise ValidationError(
                f"El profesional {self.profesional.nombre} {self.profesional.apellido} "
                f"no tiene disponibilidad los días {dia_turno}."
            )
        
        # Verificar que la hora esté dentro del rango de disponibilidad
        hora_valida = False
        for disp in disponibilidades:
            if disp.hora_inicio <= self.hora <= disp.hora_fin:
                hora_valida = True
                break
        
        if not hora_valida:
            horarios = ", ".join([
                f"{disp.hora_inicio.strftime('%H:%M')} - {disp.hora_fin.strftime('%H:%M')}"
                for disp in disponibilidades
            ])
            raise ValidationError(
                f"La hora seleccionada no está dentro de la disponibilidad del profesional. "
                f"Horarios disponibles los {dia_turno}: {horarios}"
            )
    
    class Meta:
        db_table = 'turno'
