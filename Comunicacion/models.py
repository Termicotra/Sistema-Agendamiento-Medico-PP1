from django.db import models
from Empleado.models import Empleado

class Anuncio(models.Model):
    id_anuncio = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=True, blank=True)
    titulo = models.TextField(null=False, blank=False, max_length=256)
    descripcion = models.TextField(null=True, blank=True, max_length=512)
    estado = models.TextField(null=False, blank=False, max_length=128)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=True, blank=True)
    mensaje = models.TextField(null=False, blank=False, max_length=512)
    estado = models.TextField(null=False, blank=False, max_length=128)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Notificación {self.id_notificacion} - {self.fecha}"
