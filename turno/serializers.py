from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Turno
from paciente.serializers import PacienteSerializer
from profesional.serializers import ProfesionalSerializer
from empleado.serializers import EmpleadoSerializer
from profesional.models import Profesional, Disponibilidad
from paciente.models import Paciente
from empleado.models import Empleado

class TurnoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    profesional = ProfesionalSerializer(read_only=True)
    empleado = EmpleadoSerializer(read_only=True)

    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), 
        source='paciente',
        write_only=True,
        help_text="ID del paciente asociado"
    )    
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), 
        source='profesional',
        write_only=True,
        help_text="ID del profesional asociado"
    )
    empleado_id = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all(), 
        source='empleado',
        write_only=True,
        help_text="ID del empleado asociado"
    )
    fecha = serializers.DateField(help_text="Fecha del turno")
    hora = serializers.TimeField(help_text="Hora del turno")
    estado = serializers.CharField(help_text="Estado actual del turno (pendiente, resuelto, cancelado, etc.)")
    
    class Meta:
        model = Turno
        fields = '__all__'
    
    def _validar_fecha_pasada(self, fecha):
        """Validar que la fecha no sea pasada."""
        from datetime import date
        if fecha and fecha < date.today():
            raise serializers.ValidationError({'fecha': 'No se puede ingresar una fecha pasada.'})
    
    def _validar_turnos_duplicados(self, profesional, paciente, fecha):
        """Validar que no existan turnos duplicados."""
        turnos_existentes = Turno.objects.filter(
            paciente=paciente,
            profesional=profesional,
            fecha=fecha,
            estado__in=['Pendiente', 'Activo']
        )
        
        if self.instance:
            turnos_existentes = turnos_existentes.exclude(pk=self.instance.pk)
        
        if turnos_existentes.exists():
            raise serializers.ValidationError(
                f"Ya existe un turno activo o pendiente para el paciente "
                f"{paciente.nombre} {paciente.apellido} con el profesional "
                f"{profesional.nombre} {profesional.apellido} en la fecha {fecha}."
            )
    
    def _validar_sobreposicion_profesional(self, profesional, paciente, fecha, hora):
        """Validar que no haya sobreposición de horarios para el mismo profesional (cualquier paciente)."""
        from datetime import datetime, timedelta
        
        duracion_turno = timedelta(minutes=30)
        turnos_mismo_dia = Turno.objects.filter(
            profesional=profesional,
            fecha=fecha,
            estado__in=['Pendiente', 'Activo']
        )
        
        if self.instance:
            turnos_mismo_dia = turnos_mismo_dia.exclude(pk=self.instance.pk)
        
        for turno_existente in turnos_mismo_dia:
            inicio_nuevo = datetime.combine(fecha, hora)
            fin_nuevo = inicio_nuevo + duracion_turno
            
            inicio_existente = datetime.combine(turno_existente.fecha, turno_existente.hora)
            fin_existente = inicio_existente + duracion_turno
            
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                # Si es el mismo paciente, mostrar un mensaje diferente
                if turno_existente.paciente == paciente:
                    mensaje_paciente = ""
                else:
                    mensaje_paciente = " (con otro paciente)"
                
                raise serializers.ValidationError({
                    'hora': f"El horario se solapa con otro turno del profesional "
                            f"{profesional.nombre} {profesional.apellido} "
                            f"a las {turno_existente.hora.strftime('%H:%M')} el {turno_existente.fecha}"
                            f"{mensaje_paciente}. Por favor, seleccione otro horario."
                })
    
    def _validar_sobreposicion_paciente(self, paciente, fecha, hora):
        """Validar que no haya sobreposición de horarios para el mismo paciente."""
        from datetime import datetime, timedelta
        
        duracion_turno = timedelta(minutes=30)
        turnos_paciente = Turno.objects.filter(
            paciente=paciente,
            fecha=fecha,
            estado__in=['Pendiente', 'Activo']
        )
        
        if self.instance:
            turnos_paciente = turnos_paciente.exclude(pk=self.instance.pk)
        
        for turno_existente in turnos_paciente:
            inicio_nuevo = datetime.combine(fecha, hora)
            fin_nuevo = inicio_nuevo + duracion_turno
            
            inicio_existente = datetime.combine(turno_existente.fecha, turno_existente.hora)
            fin_existente = inicio_existente + duracion_turno
            
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                raise serializers.ValidationError({
                    'hora': f"El paciente {paciente.nombre} {paciente.apellido} "
                            f"ya tiene un turno a las {turno_existente.hora.strftime('%H:%M')} "
                            f"con {turno_existente.profesional.nombre} {turno_existente.profesional.apellido}. "
                            f"Por favor, seleccione otro horario."
                })
    
    def _validar_disponibilidad_profesional(self, profesional, fecha, hora):
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
        
        dia_turno = dias_semana.get(fecha.weekday())
        
        disponibilidades = Disponibilidad.objects.filter(
            profesional=profesional,
            dia=dia_turno,
            esta_disponible=True
        )
        
        if not disponibilidades.exists():
            raise serializers.ValidationError({
                'fecha': f"El profesional {profesional.nombre} {profesional.apellido} "
                        f"no tiene disponibilidad los días {dia_turno}."
            })
        
        hora_valida = any(disp.hora_inicio <= hora <= disp.hora_fin for disp in disponibilidades)
        
        if not hora_valida:
            horarios = ", ".join([
                f"{disp.hora_inicio.strftime('%H:%M')} - {disp.hora_fin.strftime('%H:%M')}"
                for disp in disponibilidades
            ])
            raise serializers.ValidationError({
                'hora': f"La hora seleccionada no está dentro de la disponibilidad del profesional. "
                        f"Horarios disponibles los {dia_turno}: {horarios}"
            })
    
    def validate(self, data):
        """Validar disponibilidad del profesional, evitar turnos duplicados, sobreposición y fechas pasadas."""
        profesional = data.get('profesional')
        paciente = data.get('paciente')
        fecha = data.get('fecha')
        hora = data.get('hora')
        estado = data.get('estado', 'Pendiente')
        
        # Validar fecha pasada
        self._validar_fecha_pasada(fecha)
        
        if not profesional or not fecha or not hora or not paciente:
            return data
        
        # Solo validar si el turno está activo o pendiente
        if estado in ['Cancelado', 'Completado']:
            return data
        
        # Ejecutar todas las validaciones
        self._validar_turnos_duplicados(profesional, paciente, fecha)
        self._validar_sobreposicion_profesional(profesional, paciente, fecha, hora)
        self._validar_sobreposicion_paciente(paciente, fecha, hora)
        self._validar_disponibilidad_profesional(profesional, fecha, hora)
        
        return data
