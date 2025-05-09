from django.db import models

class Secretario(models.Model):
    id_secretario = models.AutoField(primary_key=True)
    ci = models.TextField()
    nombre = models.TextField()
    apellido = models.TextField()
    fecha_nacimiento = models.TextField()
    direccion = models.TextField()
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
