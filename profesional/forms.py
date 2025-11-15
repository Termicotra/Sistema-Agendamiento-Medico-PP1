from django import forms
from profesional.models import Profesional, Disponibilidad

class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 
                 'especialidad', 'registro_profesional', 'otro_contacto']
        labels = {
            'ci': 'Cédula de Identidad',
            'fecha_nacimiento': 'Fecha de nacimiento (día/mes/año)',
        }

from profesional.models import Profesional
class DisponibilidadForm(forms.ModelForm):
    especialidad = forms.ChoiceField(label='Especialidad', required=False)

    class Meta:
        model = Disponibilidad
        fields = ['dia', 'hora_inicio', 'hora_fin', 'esta_disponible', 'especialidad', 'profesional']
        widgets = {
            'dia': forms.Select(choices=Disponibilidad.DIAS_SEMANA),
        }
        labels = {
            'hora_inicio': 'Hora de inicio (hh:mm)',
            'hora_fin': 'Hora de fin (hh:mm)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        especialidades = Profesional.objects.values_list('especialidad', flat=True).distinct()
        self.fields['especialidad'].choices = [('', 'Seleccione una especialidad')] + [(e, e) for e in especialidades]
        selected_especialidad = self.data.get('especialidad') or self.initial.get('especialidad')
        if selected_especialidad:
            self.fields['profesional'].queryset = Profesional.objects.filter(especialidad=selected_especialidad)
        else:
            self.fields['profesional'].queryset = Profesional.objects.none()
