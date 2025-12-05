from django.db import models


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    ci = models.CharField(null=False, blank=False, max_length=128)
    nombre = models.CharField(null=False, blank=False, max_length=128)
    apellido = models.CharField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.CharField(blank=True, max_length=128, default='')
    telefono = models.CharField(blank=True, max_length=128, default='')
    cargo = models.CharField(null=False, blank=False, max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"
    
    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'