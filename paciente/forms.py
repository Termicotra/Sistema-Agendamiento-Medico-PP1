from django import forms
from paciente.models import Paciente, HistorialClinico, ReporteMedico

"""class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']
        labels = {
            'ci': 'Cédula de Identidad',
            'fecha_nacimiento': 'Fecha de nacimiento (día/mes/año)',
        }
        widgets = {}"""

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'ci', 'fecha_nacimiento',
'telefono', 'direccion']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'ci': 'Cédula',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class':
'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = [
            'fecha',
            'hora',
            'razon',
            'descripcion',
            'paciente',
            'profesional',
        ]
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }

class ReporteMedicoForm(forms.ModelForm):
    class Meta:
        model = ReporteMedico
        fields = [
            'fecha',
            'descripcion',
            'paciente',
            'profesional',
        ]
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }