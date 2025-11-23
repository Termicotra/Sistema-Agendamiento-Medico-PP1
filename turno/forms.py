from django import forms
from turno.models import Turno
from profesional.models import Profesional, Disponibilidad

class TurnoForm(forms.ModelForm):
    # Helper field for filtering professionals by specialty - not persisted to the database
    especialidad = forms.ChoiceField(label='Especialidad', required=False)

    class Meta:
        model = Turno
        fields = ['paciente', 'fecha', 'hora', 'modalidad', 'motivo', 'fue_notificado', 'especialidad', 'profesional', 'empleado']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
            'hora': 'Hora (hh:mm)',
            'ci': 'Cédula de Identidad',
            'paciente': 'Paciente',
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
            # Mostrar todos los profesionales si no hay especialidad seleccionada
            self.fields['profesional'].queryset = Profesional.objects.all()
        # Hacer opcional el campo empleado
        self.fields['empleado'].required = False
        # Si el usuario es paciente, hacer el campo paciente de solo lectura
        if self.request and self.request.user.groups.filter(name__iexact='pacientes').exists():
            self.fields['paciente'].disabled = True
            self.fields['paciente'].widget.attrs['readonly'] = True

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        from datetime import date
        if fecha and fecha < date.today():
            raise forms.ValidationError('No se puede ingresar una fecha pasada.')
        return fecha
