from django import forms
from turno.models import Turno

from profesional.models import Profesional
class TurnoForm(forms.ModelForm):
    especialidad = forms.ChoiceField(label='Especialidad', required=False)

    class Meta:
        model = Turno
        fields = ['fecha', 'hora', 'modalidad', 'motivo', 'fue_notificado', 'especialidad', 'profesional', 'empleado']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
            'hora': 'Hora (hh:mm)',
            'ci': 'Cédula de Identidad',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Especialidades únicas
        especialidades = Profesional.objects.values_list('especialidad', flat=True).distinct()
        self.fields['especialidad'].choices = [('', 'Seleccione una especialidad')] + [(e, e) for e in especialidades]
        # Filtrar profesionales por especialidad seleccionada
        selected_especialidad = self.data.get('especialidad') or self.initial.get('especialidad')
        if selected_especialidad:
            self.fields['profesional'].queryset = Profesional.objects.filter(especialidad=selected_especialidad)
        else:
            self.fields['profesional'].queryset = Profesional.objects.none()
