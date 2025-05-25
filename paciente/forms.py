from django import forms
from paciente.models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']