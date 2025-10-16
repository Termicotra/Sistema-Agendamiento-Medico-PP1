from rest_framework import serializers
from .models import Turno
from .models import RecordatorioTurno
from paciente.serializers import PacienteSerializer
from profesional.serializers import ProfesionalSerializer
from empleado.serializers import EmpleadoSerializer
from profesional.models import Profesional
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

class RecordatorioTurnoSerializer(serializers.ModelSerializer):
    turno = TurnoSerializer(read_only=True)
    paciente = PacienteSerializer(read_only=True)
    turno_id = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all(), 
        source='turno',
        write_only=True,
        help_text="ID del turno asociado"
    )
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), 
        source='paciente',
        write_only=True,
        help_text="ID del paciente asociado"
    )
    fecha_envio = serializers.DateField()
    hora_envio = serializers.TimeField()
    mensaje = serializers.CharField(max_length=512)
    enviado = serializers.BooleanField()

    class Meta:
        model = RecordatorioTurno
        fields = '__all__'

