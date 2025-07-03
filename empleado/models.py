from django.db import models

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    ci = models.CharField(null=False, blank=False)
    nombre = models.CharField(null=False, blank=False)
    apellido = models.CharField(null=False, blank=False)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.CharField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    cargo = models.CharField(null=False, blank=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"
