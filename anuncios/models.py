from django.db import models
from secretarios.models import Secretario

class Anuncio(models.Model):
    id_anuncio = models.AutoField(primary_key=True)
    fecha = models.TextField()
    hora = models.TextField()
    titulo = models.TextField()
    descripcion = models.TextField()
    secretario = models.ForeignKey(Secretario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
