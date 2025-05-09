from django.db import models

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    ci = models.TextField()
    nombre = models.TextField()
    apellido = models.TextField()
    fecha_nacimiento = models.IntegerField()  # Using IntegerField as per diagram
    direccion = models.TextField()
    telefono = models.IntegerField()
    otro_contacto = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
