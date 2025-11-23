from django.db import models
from django.conf import settings


class SolicitudRegistro(models.Model):
	"""Solicitudes de registro pendientes de aprobación por el administrador."""
	ESTADO_CHOICES = [
		('pendiente', 'Pendiente'),
		('aprobada', 'Aprobada'),
		('rechazada', 'Rechazada'),
	]
	
	username = models.CharField(max_length=150, unique=True)
	password_hash = models.CharField(max_length=255)  # Almacena password hasheado
	ci = models.CharField(max_length=20, unique=True)
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
	fecha_solicitud = models.DateTimeField(auto_now_add=True)
	fecha_procesada = models.DateTimeField(null=True, blank=True)
	procesada_por = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.SET_NULL, 
		null=True, 
		blank=True, 
		related_name='solicitudes_procesadas'
	)
	
	class Meta:
		db_table = 'solicitud_registro'
		ordering = ['-fecha_solicitud']
		verbose_name = 'Solicitud de Registro'
		verbose_name_plural = 'Solicitudes de Registro'
	
	def __str__(self):
		return f"Solicitud {self.username} - {self.get_estado_display()}"
