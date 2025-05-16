from django.db import models

class Profesional(models.Model):
    id_profesional = models.AutoField(primary_key=True)
    ci = models.TextField(null=False, blank=False, max_length=128)
    nombre = models.TextField(null=False, blank=False, max_length=128)
    apellido = models.TextField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.TextField(null=True, blank=True, max_length=256)
    telefono = models.TextField(null=False, blank=False, max_length=30)
    especialidad = models.TextField(null=False, blank=False, max_length=256)
    registro_profesional = models.TextField(null=False, blank=False, max_length=256)
    otro_contacto = models.TextField(null=True, blank=True, max_length=254)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Disponibilidad(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    dia = models.DateField(null=False, blank=False)
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_fin = models.TimeField(null=False, blank=False)
    esta_disponible = models.BooleanField(null=False, blank=False, default=True)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.profesional} - {self.dia} ({self.hora_inicio}-{self.hora_fin})"
