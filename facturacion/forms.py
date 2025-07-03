from django import forms
from facturacion.models import Facturacion, DetalleFactura
from turno.models import Turno

class FacturacionForm(forms.ModelForm):
    class Meta:
        model = Facturacion
        fields = ['fecha', 'monto_total', 'metodo_pago', 'tipo_facturacion', 'turno']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'turno' in self.fields:
            self.fields['turno'].queryset = Turno.objects.filter(estado='Activo')

class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['monto', 'descripción', 'descuento', 'factura']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'factura' in self.fields:
            self.fields['factura'].queryset = Facturacion.objects.filter(estado='Pendiente')
