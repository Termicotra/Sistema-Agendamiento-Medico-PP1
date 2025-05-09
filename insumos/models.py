from django.db import models

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre = models.TextField()
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    fecha_caducidad = models.TextField()
    laboratorio = models.TextField()

    def __str__(self):
        return self.nombre
