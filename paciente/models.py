from django.db import models
from profesional.models import Profesional


class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    ci = models.CharField(null=False, blank=False, max_length=128)
    nombre = models.CharField(null=False, blank=False, max_length=128)
    apellido = models.CharField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)  
    direccion = models.CharField(blank=True, max_length=128, default='')
    telefono = models.CharField(null=False, blank=False, max_length=128)
    otro_contacto = models.CharField(blank=True, max_length=256, default='')

    def __str__(self):
        return f"{self.nombre} {self.apellido} (CI: {self.ci})"
    
    class Meta:
        db_table = 'paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


class HistorialClinico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    razon = models.CharField(null=False, blank=False, max_length=512)
    descripcion = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return (f"Historial de {self.paciente.nombre} {self.paciente.apellido} - "
                f"{self.profesional.nombre} {self.profesional.apellido} ({self.fecha})")
    
    class Meta:
        db_table = 'historial_clinico'
        verbose_name = 'Historial Clínico'
        verbose_name_plural = 'Historiales Clínicos'


class ReporteMedico(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False, max_length=512)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False, blank=False, default=None)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return (f"Reporte de {self.paciente.nombre} {self.paciente.apellido} - "
                f"{self.profesional.nombre} {self.profesional.apellido} ({self.fecha})")
    
    class Meta:
        db_table = 'reporte_medico'
        verbose_name = 'Reporte Médico'
        verbose_name_plural = 'Reportes Médicos'