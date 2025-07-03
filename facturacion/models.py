from django.db import models
from turno.models import Turno

class Facturacion(models.Model):
    class MetodoPagoFacturacionChoices(models.TextChoices):
        TARJETA_CREDITO = 'Tarjeta Crédito', 'Trajeta Crédito'
        TARJETA_DEBITO = 'Tarjeta Débito', 'Tarjeta Débito'
        EFECTIVO = 'Efectivo', 'Efectivo'
        SEGURO = 'Seguro', 'Seguro'

    class EstadoFacturacionChoices(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        PAGADO = 'Pagado', 'Pagado'
        ANULADO = 'Anulado', 'Anulado'

    id_facturacion = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    monto_total = models.IntegerField(null=False, blank=False)
    metodo_pago = models.CharField(
        choices=MetodoPagoFacturacionChoices.choices,
        default=MetodoPagoFacturacionChoices.EFECTIVO
    )
    tipo_facturacion = models.IntegerField(null=False, blank=False)
    estado = models.CharField(
        choices=EstadoFacturacionChoices.choices,
        default=EstadoFacturacionChoices.PENDIENTE
    )
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return f"Factura {self.fecha} {self.turno.paciente} - {self.estado}"
    
class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    monto = models.IntegerField(null=False, blank=False)
    descripción = models.CharField(null=False, blank=False, max_length=512)
    descuento = models.IntegerField(null=True, blank=True)
    factura = models.ForeignKey(Facturacion, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return f"Detalle {self.id_detalle_factura} de la Factura {self.factura.id_facturacion}"
