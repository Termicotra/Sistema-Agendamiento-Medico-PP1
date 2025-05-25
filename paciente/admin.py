from django.contrib import admin
from .models import Paciente
from .models import HistorialClinico
from .models import ReporteMedico

admin.site.register(ReporteMedico)
admin.site.register(HistorialClinico)
#admin.site.register(Paciente)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('ci', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'direccion')
    search_fields = ('ci', 'nombre', 'apellido')
    ordering = ('ci',)
    list_per_page = 10
