from django import forms
from profesional.models import Profesional, Disponibilidad

class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 
                 'especialidad', 'registro_profesional', 'otro_contacto']

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['dia', 'hora_inicio', 'hora_fin', 'esta_disponible', 'profesional']
        widgets = {
            'dia': forms.Select(choices=Disponibilidad.DIAS_SEMANA),
        }
