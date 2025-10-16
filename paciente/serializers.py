from rest_framework import serializers
from .models import Paciente
from .models import HistorialClinico
from .models import ReporteMedico
from profesional.models import Profesional
from profesional.serializers import ProfesionalSerializer

class PacienteSerializer(serializers.ModelSerializer):
    ci = serializers.CharField(help_text="Cédula de identidad del paciente")
    nombre = serializers.CharField(help_text="Nombre del paciente")
    apellido = serializers.CharField(help_text="Apellido del paciente")
    fecha_nacimiento = serializers.DateField(help_text="Fecha de nacimiento del paciente")
    direccion = serializers.CharField(help_text="Dirección del paciente", required=False, allow_blank=True)
    telefono = serializers.CharField(help_text="Teléfono de contacto principal")
    otro_contacto = serializers.CharField(help_text="Otro medio de contacto", required=False, allow_blank=True)

    class Meta:
        model = Paciente
        fields = '__all__'

class HistorialClinicoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    profesional = ProfesionalSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='paciente', write_only=True, help_text="ID del paciente asociado")
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), source='profesional', write_only=True, help_text="ID del profesional asociado")
    fecha = serializers.DateField(help_text="Fecha del historial clínico")
    hora = serializers.TimeField(help_text="Hora del historial clínico")
    razon = serializers.CharField(help_text="Razón de la consulta o atención")
    descripcion = serializers.CharField(help_text="Descripción detallada del historial clínico")

    class Meta:
        model = HistorialClinico
        fields = '__all__'

class ReporteMedicoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    profesional = ProfesionalSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='paciente', write_only=True, help_text="ID del paciente asociado")
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), source='profesional', write_only=True, help_text="ID del profesional asociado")
    fecha = serializers.DateField(help_text="Fecha del reporte médico")
    descripcion = serializers.CharField(help_text="Descripción detallada del reporte médico")

    class Meta:
        model = ReporteMedico
        fields = '__all__'
