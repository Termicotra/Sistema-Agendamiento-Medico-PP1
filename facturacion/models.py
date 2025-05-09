from django.db import models
from turnos.models import Turno

class Facturacion(models.Model):
    id_factura = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    monto = models.IntegerField()
    metodo_pago = models.TextField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura {self.id_factura} - {self.fecha}"
