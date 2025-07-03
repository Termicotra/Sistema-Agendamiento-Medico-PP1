from django import forms
from facturacion.models import Facturacion, DetalleFactura

class FacturacionForm(forms.ModelForm):
    class Meta:
        model = Facturacion
        fields = ['fecha', 'monto_total', 'metodo_pago', 'tipo_facturacion', 'estado', 'turno']
        labels = {
            'fecha': 'Fecha (día/mes/año)',
        }

class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['monto', 'descripción', 'descuento', 'factura']
