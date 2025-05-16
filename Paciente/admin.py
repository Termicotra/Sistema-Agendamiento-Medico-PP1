from django.contrib import admin
from .models import Paciente
from .models import HistorialClinico
from .models import ReporteMedico

admin.site.register(ReporteMedico)
admin.site.register(HistorialClinico)
admin.site.register(Paciente)
