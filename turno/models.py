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
        max_length=20,
        choices=ModalidadTurnoChoices.choices,
        default=ModalidadTurnoChoices.PRESENCIAL
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoTurnoChoices.choices,
        default=EstadoTurnoChoices.PENDIENTE
    )
    motivo = models.TextField(null=False, blank=False, max_length=128)
    fue_notificado = models.BooleanField(null=False, blank=False, default=False)
    profesional = models.ForeignKey(
        Profesional, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False, 
        default=None,
        related_name='turnos'
    )
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False, 
        default=None,
        related_name='turnos'
    )
    empleado = models.ForeignKey(
        Empleado, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        default=None,
        related_name='turnos_gestionados'
    )

    def __str__(self):
        return (f"Turno de {self.paciente.nombre} {self.paciente.apellido} - "
                f"{self.profesional.especialidad} ({self.fecha} {self.hora})")
    
    def _validar_turnos_duplicados(self):
        """Validar que no existan turnos duplicados para el mismo paciente y profesional."""
        turnos_existentes = Turno.objects.filter(
            paciente=self.paciente,
            profesional=self.profesional,
            fecha=self.fecha,
            estado__in=[self.EstadoTurnoChoices.PENDIENTE, self.EstadoTurnoChoices.ACTIVO]
        )
        
        if self.pk:
            turnos_existentes = turnos_existentes.exclude(pk=self.pk)
        
        if turnos_existentes.exists():
            raise ValidationError(
                f"Ya existe un turno activo o pendiente para el paciente "
                f"{self.paciente.nombre} {self.paciente.apellido} con el profesional "
                f"{self.profesional.nombre} {self.profesional.apellido} en la fecha {self.fecha}."
            )
    
    def _validar_sobreposicion_profesional(self):
        """Validar que no haya sobreposición de horarios para el mismo profesional."""
        from datetime import datetime, timedelta
        
        duracion_turno = timedelta(minutes=30)
        turnos_mismo_dia = Turno.objects.filter(
            profesional=self.profesional,
            fecha=self.fecha,
            estado__in=[self.EstadoTurnoChoices.PENDIENTE, self.EstadoTurnoChoices.ACTIVO]
        )
        
        if self.pk:
            turnos_mismo_dia = turnos_mismo_dia.exclude(pk=self.pk)
        
        for turno_existente in turnos_mismo_dia:
            inicio_nuevo = datetime.combine(self.fecha, self.hora)
            fin_nuevo = inicio_nuevo + duracion_turno
            
            inicio_existente = datetime.combine(turno_existente.fecha, turno_existente.hora)
            fin_existente = inicio_existente + duracion_turno
            
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                mensaje_paciente = "" if turno_existente.paciente == self.paciente else " (con otro paciente)"
                
                raise ValidationError(
                    f"El horario se solapa con otro turno del profesional "
                    f"{self.profesional.nombre} {self.profesional.apellido} "
                    f"a las {turno_existente.hora.strftime('%H:%M')} el {turno_existente.fecha}"
                    f"{mensaje_paciente}. Por favor, seleccione otro horario."
                )
    
    def _validar_sobreposicion_paciente(self):
        """Validar que no haya sobreposición de horarios para el mismo paciente."""
        from datetime import datetime, timedelta
        
        duracion_turno = timedelta(minutes=30)
        turnos_paciente = Turno.objects.filter(
            paciente=self.paciente,
            fecha=self.fecha,
            estado__in=[self.EstadoTurnoChoices.PENDIENTE, self.EstadoTurnoChoices.ACTIVO]
        )
        
        if self.pk:
            turnos_paciente = turnos_paciente.exclude(pk=self.pk)
        
        for turno_existente in turnos_paciente:
            inicio_nuevo = datetime.combine(self.fecha, self.hora)
            fin_nuevo = inicio_nuevo + duracion_turno
            
            inicio_existente = datetime.combine(turno_existente.fecha, turno_existente.hora)
            fin_existente = inicio_existente + duracion_turno
            
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                raise ValidationError(
                    f"El paciente {self.paciente.nombre} {self.paciente.apellido} "
                    f"ya tiene un turno a las {turno_existente.hora.strftime('%H:%M')} "
                    f"con {turno_existente.profesional.nombre} {turno_existente.profesional.apellido}. "
                    f"Por favor, seleccione otro horario."
                )
    
    def _validar_disponibilidad_profesional(self):
        """Validar que el profesional tenga disponibilidad en el día y hora solicitados."""
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
        
        hora_valida = any(
            disp.hora_inicio <= self.hora <= disp.hora_fin 
            for disp in disponibilidades
        )
        
        if not hora_valida:
            horarios = ", ".join([
                f"{disp.hora_inicio.strftime('%H:%M')} - {disp.hora_fin.strftime('%H:%M')}"
                for disp in disponibilidades
            ])
            raise ValidationError(
                f"La hora seleccionada no está dentro de la disponibilidad del profesional. "
                f"Horarios disponibles los {dia_turno}: {horarios}"
            )
    
    def clean(self):
        """Validar disponibilidad del profesional, evitar turnos duplicados y sobreposición de horarios."""
        super().clean()
        
        if not all([self.profesional, self.fecha, self.hora, self.paciente]):
            return
        
        # Solo validar si el turno está activo o pendiente
        if self.estado in [self.EstadoTurnoChoices.CANCELADO, self.EstadoTurnoChoices.COMPLETADO]:
            return
        
        # Ejecutar todas las validaciones
        self._validar_turnos_duplicados()
        self._validar_sobreposicion_profesional()
        self._validar_sobreposicion_paciente()
        self._validar_disponibilidad_profesional()
    
    class Meta:
        db_table = 'turno'
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['-fecha', '-hora']

class RecordatorioTurno(models.Model):
    id_recordatorio = models.AutoField(primary_key=True)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=False, blank=False, related_name='recordatorios')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, related_name='recordatorios')
    fecha_envio = models.DateField()
    hora_envio = models.TimeField()
    mensaje = models.TextField(max_length=512)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"Recordatorio para {self.paciente.nombre} {self.paciente.apellido} - Turno {self.turno.id_turno} - Enviado: {self.enviado}"
