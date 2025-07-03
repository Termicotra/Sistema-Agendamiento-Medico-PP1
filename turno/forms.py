from django import forms
from turno.models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'hora', 'modalidad', 'estado', 'motivo', 'fue_notificado', 
                 'profesional', 'paciente', 'empleado']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
            'hora': 'Hora (hh:mm)',
            'ci': 'Cédula de Identidad',
        }
