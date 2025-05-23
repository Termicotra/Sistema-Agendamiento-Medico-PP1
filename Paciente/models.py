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
    telefono = models.TextField(null=False, blank=False, max_length=128)
    otro_contacto = models.TextField(null=True, blank=True, max_length=256)

    def __str__(self):
        return f"CI: {self.ci} {self.nombre} {self.apellido}"
    
class HistorialClinico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    razon = models.TextField(null=False, blank=False, max_length=512)
    nota = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return (f"Historial Paciente: {self.paciente.nombre} {self.paciente.apellido} con CI {self.paciente.ci} "
                f"el {self.fecha} a las {self.hora} con Profesional: {self.profesional.nombre} {self.profesional.apellido} {self.profesional.ci} "
                f" con Especialidad {self.profesional.especialidad} ")
    
class ReporteMedico(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return (f"Reporte Paciente: {self.paciente.nombre} {self.paciente.apellido} con CI {self.paciente.ci} "
                f"el {self.fecha} con Profesional: {self.profesional.nombre} {self.profesional.apellido} {self.profesional.ci} "
                f" con Especialidad {self.profesional.especialidad} ")
