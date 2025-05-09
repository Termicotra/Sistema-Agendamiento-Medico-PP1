from django.db import models
from turnos.models import Turno

class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    mensaje = models.TextField()
    estado = models.TextField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notificación {self.id_notificacion} - {self.fecha}"
