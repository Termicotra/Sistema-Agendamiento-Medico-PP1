from rest_framework import serializers
from .models import Empleado

class EmpleadoSerializer(serializers.ModelSerializer):
    ci = serializers.CharField(help_text="Cédula de identidad del empleado")
    nombre = serializers.CharField(help_text="Nombre del empleado")
    apellido = serializers.CharField(help_text="Apellido del empleado")
    fecha_nacimiento = serializers.DateField(help_text="Fecha de nacimiento del empleado")
    direccion = serializers.CharField(help_text="Dirección del empleado", required=False, allow_blank=True)
    telefono = serializers.CharField(help_text="Teléfono de contacto principal")
    otro_contacto = serializers.CharField(help_text="Otro medio de contacto", required=False, allow_blank=True)
    
    class Meta:
        model = Empleado
        fields = '__all__'