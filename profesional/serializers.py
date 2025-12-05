from rest_framework import serializers
from .models import Profesional
from .models import Disponibilidad

class ProfesionalSerializer(serializers.ModelSerializer):
    ci = serializers.CharField(help_text="Cédula de identidad del profesional")
    nombre = serializers.CharField(help_text="Nombre del profesional")
    apellido = serializers.CharField(help_text="Apellido del profesional")
    especialidad = serializers.CharField(help_text="Especialidad médica del profesional")
    registro_profesional = serializers.CharField(help_text="Registro profesional del médico")
    fecha_nacimiento = serializers.DateField(help_text="Fecha de nacimiento del profesional")
    direccion = serializers.CharField(help_text="Dirección del profesional", required=False, allow_blank=True)
    telefono = serializers.CharField(help_text="Teléfono de contacto principal")
    otro_contacto = serializers.CharField(help_text="Otro medio de contacto", required=False, allow_blank=True)
    
    class Meta:
        model = Profesional
        exclude = ['user']  # Excluir el campo user

class DisponibilidadSerializer(serializers.ModelSerializer):
    profesional = ProfesionalSerializer(read_only=True)
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), source='profesional', write_only=True, help_text="ID del profesional asociado")
    dia = serializers.CharField(help_text="Día de la semana de la disponibilidad")
    hora_inicio = serializers.TimeField(help_text="Hora de inicio de la disponibilidad")
    hora_fin = serializers.TimeField(help_text="Hora de fin de la disponibilidad")
    
    class Meta:
        model = Disponibilidad
        fields = '__all__'