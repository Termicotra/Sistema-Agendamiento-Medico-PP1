from django.db import models

class Profesional(models.Model):
    id_profesional = models.AutoField(primary_key=True)
    ci = models.CharField(null=False, blank=False, max_length=128)
    nombre = models.CharField(null=False, blank=False, max_length=128)
    apellido = models.CharField(null=False, blank=False, max_length=128)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    direccion = models.CharField(null=True, blank=True, max_length=256)
    telefono = models.CharField(null=False, blank=False, max_length=128)
    especialidad = models.CharField(null=False, blank=False, max_length=256)
    registro_profesional = models.CharField(null=False, blank=False, max_length=256)
    otro_contacto = models.CharField(null=True, blank=True, max_length=254)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad} "


class Disponibilidad(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    DIAS_SEMANA = [
        ("Lunes", "Lunes"),
        ("Martes", "Martes"),
        ("Miercoles", "Miércoles"),
        ("Jueves", "Jueves"),
        ("Sabado", "Sábado"),
        ("Domingo", "Domingo"),
    ]
    dia = models.CharField(max_length=16, choices=DIAS_SEMANA, null=False, blank=False)
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_fin = models.TimeField(null=False, blank=False)
    esta_disponible = models.BooleanField(null=False, blank=False, default=True)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=False, blank=False, default=None)

    def __str__(self):
        return (f"{self.profesional.nombre} {self.profesional.apellido} - {self.profesional.especialidad}")
