from django.db import models

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    ci = models.TextField(null=False, blank=False)
    nombre = models.TextField(null=False, blank=False)
    apellido = models.TextField(null=False, blank=False)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    cargo = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
