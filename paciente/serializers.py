from rest_framework import serializers
from .models import Paciente
from .models import HistorialClinico
from .models import ReporteMedico
from profesional.models import Profesional
from profesional.serializers import ProfesionalSerializer

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__' 

class HistorialClinicoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    profesional = ProfesionalSerializer(read_only=True)

    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), 
        source='paciente',
        write_only=True
    )    
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), 
        source='profesional',
        write_only=True
    )
    
    class Meta:
        model = HistorialClinico
        fields = '__all__'

class ReporteMedicoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    profesional = ProfesionalSerializer(read_only=True)

    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), 
         source='paciente',
         write_only=True
    )
    profesional_id = serializers.PrimaryKeyRelatedField(queryset=Profesional.objects.all(), 
        source='profesional',
        write_only=True
    )
    
    class Meta:
        model = ReporteMedico
        fields = '__all__'
