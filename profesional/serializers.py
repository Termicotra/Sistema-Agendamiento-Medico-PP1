from rest_framework import serializers
from .models import Profesional
from .models import Disponibilidad

class ProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesional
        fields = '__all__'

class DisponibilidadSerializer(serializers.ModelSerializer):
    profesional = ProfesionalSerializer(read_only=True)
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), 
        source='profesional', write_only=True)
    
    class Meta:
        model = Disponibilidad
        fields = '__all__'