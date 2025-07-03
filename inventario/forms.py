from django import forms
from inventario.models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad', 'fecha_caducidad', 'laboratorio']
        labels = {
            'fecha_caducidad': 'Fecha de caducidad (día/mes/año)',
        }
