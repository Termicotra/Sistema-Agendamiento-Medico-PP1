from django.db import models

class Profesional(models.Model):
    id_profesional = models.AutoField(primary_key=True)
    ci = models.TextField()
    nombre = models.TextField()
    apellido = models.TextField()
    fecha_nacimiento = models.TextField()
    direccion = models.TextField()
    telefono = models.IntegerField()
    especialidad = models.TextField()
    registro_profesional = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
