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
    
    def validate(self, data):
        """Validar que la fecha y hora coincidan con la disponibilidad del profesional."""
        profesional = data.get('profesional')
        fecha = data.get('fecha')
        hora = data.get('hora')
        
        if profesional and fecha and hora:
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
            
            dia_turno = dias_semana.get(fecha.weekday())
            
            # Buscar disponibilidad del profesional para ese día
            disponibilidades = Disponibilidad.objects.filter(
                profesional=profesional,
                dia=dia_turno,
                esta_disponible=True
            )
            
            if not disponibilidades.exists():
                raise serializers.ValidationError(
                    f"El profesional {profesional.nombre} {profesional.apellido} "
                    f"no tiene disponibilidad los días {dia_turno}."
                )
            
            # Verificar que la hora esté dentro del rango de disponibilidad
            hora_valida = False
            for disp in disponibilidades:
                if disp.hora_inicio <= hora <= disp.hora_fin:
                    hora_valida = True
                    break
            
            if not hora_valida:
                horarios = ", ".join([
                    f"{disp.hora_inicio.strftime('%H:%M')} - {disp.hora_fin.strftime('%H:%M')}"
                    for disp in disponibilidades
                ])
                raise serializers.ValidationError(
                    f"La hora seleccionada no está dentro de la disponibilidad del profesional. "
                    f"Horarios disponibles los {dia_turno}: {horarios}"
                )
        
        return data
