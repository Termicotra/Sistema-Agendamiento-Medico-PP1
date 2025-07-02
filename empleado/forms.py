from django import forms
from empleado.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'direccion', 'telefono', 'cargo']
