from django import forms
from paciente.models import Paciente, HistorialClinico, ReporteMedico


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']
        labels = {
            'ci': 'Cédula de Identidad',
            'fecha_nacimiento': 'Fecha de nacimiento (día/mes/año)',
        }


class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = '__all__'
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }


class ReporteMedicoForm(forms.ModelForm):
    class Meta:
        model = ReporteMedico
        fields = '__all__'
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }