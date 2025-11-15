from django.db import models

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    ci = models.CharField(null=False, blank=False, max_length=128)
    nombre = models.CharField(null=False, blank=False, max_length=128)
    apellido = models.CharField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.CharField(null=True, blank=True, max_length=128)
    telefono = models.CharField(null=True, blank=True)
    cargo = models.CharField(null=False, blank=False, max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    class Meta:
        db_table = 'empleado'