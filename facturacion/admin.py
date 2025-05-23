from django.contrib import admin
from .models import Facturacion
from .models import DetalleFactura

admin.site.register(DetalleFactura)
admin.site.register(Facturacion)
