from django import forms
from turno.models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'hora', 'modalidad', 'motivo', 'fue_notificado', 
                 'profesional', 'paciente', 'empleado']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
            'hora': 'Hora (hh:mm)',
            'ci': 'Cédula de Identidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si en algún campo se referencia a turnos, filtrar solo activos
        for field_name, field in self.fields.items():
            if hasattr(field, 'queryset') and field.queryset.model.__name__ == 'Turno':
                field.queryset = field.queryset.filter(estado='Activo')
