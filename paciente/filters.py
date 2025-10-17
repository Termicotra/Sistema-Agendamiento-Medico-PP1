import django_filters
from .models import Paciente, HistorialClinico, ReporteMedico

class PacienteFilter(django_filters.FilterSet):
    #Filtro de Paciente
    id__paciente = django_filters.NumberFilter(label='ID del Paciente')
    nombre = django_filters.CharFilter(label='Nombre del Paciente' , lookup_expr='icontains')
    apellido = django_filters.CharFilter(label='Apellido del Paciente', lookup_expr='icontains')
    ci = django_filters.CharFilter(label='CI del Paciente', lookup_expr='icontains')

    class Meta:
        model = Paciente
        fields = ['id__paciente', 'nombre', 'apellido', 'ci']

class HistorialClinicoFilter(django_filters.FilterSet):
    #Filtro de Historial Clinico
    historialclinico__fecha = django_filters.DateFilter(field_name='fecha',label='Fecha del Historial Clinico', lookup_expr='icontains')
    id__paciente = django_filters.NumberFilter(field_name='paciente__id_paciente', label='ID del Paciente')
    historialclinico__paciente__nombre = django_filters.CharFilter(field_name='paciente__nombre', label='Nombre del Paciente', lookup_expr='icontains')
    historialclinico__paciente__apellido = django_filters.CharFilter(field_name='paciente__apellido', label='Apellido del Paciente', lookup_expr='icontains')
    historialclinico__paciente__ci = django_filters.CharFilter(field_name='paciente__ci', label='CI del Paciente', lookup_expr='icontains')
    historialclinico__profesional__nombre = django_filters.CharFilter(field_name='profesional__nombre', label='Nombre del Profesional', lookup_expr='icontains')
    historialclinico__profesional__apellido = django_filters.CharFilter(field_name='profesional__apellido', label='Apellido del Profesional', lookup_expr='icontains')

    class Meta:
        model = HistorialClinico
        fields = ['historialclinico__fecha', 'id__paciente', 
                  'historialclinico__paciente__nombre', 'historialclinico__paciente__apellido',
                    'historialclinico__paciente__ci', 'historialclinico__profesional__nombre', 
                    'historialclinico__profesional__apellido']
    
