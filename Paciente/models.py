from django.db import models
from Profesional.models import Profesional
from Inventario.models import Insumo

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    ci = models.TextField(null=False, blank=False, max_length=128)
    nombre = models.TextField(null=False, blank=False, max_length=128)
    apellido = models.TextField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)  
    direccion = models.TextField(null=True, blank=True, max_length=128)
    telefono = models.IntegerField(null=False, blank=False)
    otro_contacto = models.IntegerField(null=True, blank=True, max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class HistorialClinico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.DateTimeField(null=False, blank=False)
    razon = models.TextField(null=False, blank=False, max_length=512)
    nota = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Historial {self.id_historial} - Paciente: {self.paciente}"
    
class ReporteMedico(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha}"
