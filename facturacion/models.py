from django.db import models
from Turno.models import Turno

class Facturacion(models.Model):
    id_facturacion = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    monto_total = models.IntegerField(null=False, blank=False)
    metodo_pago = models.TextField(null=False, blank=False, max_length=128)
    tipo_facturacion = models.IntegerField(null=False, blank=False)
    estado = models.TextField(null=False, blank=False, max_length=128)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Factura {self.id_factura} - {self.fecha}"
    
class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    monto = models.IntegerField(null=False, blank=False)
    descripción = models.TextField(null=False, blank=False, max_length=512)
    descuento = models.IntegerField(null=True, blank=True)
    factura = models.ForeignKey(Facturacion, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Factura {self.factura.id_factura}"
