from django import forms
from empleado.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 'cargo']
        labels = {
            'ci': 'Cédula de Identidad',
            'fecha_nacimiento': 'Fecha de nacimiento (día/mes/año)',
        }
