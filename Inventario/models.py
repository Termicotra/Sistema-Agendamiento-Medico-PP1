from django.db import models

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre = models.TextField(null=False, blank=False, max_length=128)
    descripcion = models.TextField(null=False, blank=False, max_length=128)
    cantidad = models.IntegerField(null=False, blank=False)
    fecha_caducidad = models.DateField(null=False, blank=False)
    laboratorio = models.TextField(null=False, blank=False, max_length=128)

    def __str__(self):
        return self.nombre
