from django import forms
from paciente.models import Paciente, HistorialClinico, ReporteMedico


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ci', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion']


class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = '__all__'


class ReporteMedicoForm(forms.ModelForm):
    class Meta:
        model = ReporteMedico
        fields = '__all__'