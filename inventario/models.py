from django.db import models

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, blank=False, max_length=128)
    descripcion = models.CharField(null=False, blank=False, max_length=128)
    cantidad = models.IntegerField(null=False, blank=False)
    fecha_caducidad = models.DateField(null=False, blank=False)
    laboratorio = models.CharField(null=False, blank=False, max_length=128)

    def __str__(self):
        return (f"{self.nombre} {self.laboratorio}")
