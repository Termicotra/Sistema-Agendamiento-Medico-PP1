"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from paciente import views
from empleado import views as empleado_views
from profesional import views as profesional_views
from turno import views as turno_views
from django.shortcuts import render
from paciente import views as paciente_views
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schemaView = get_schema_view(
    openapi.Info(
        title="API de Sistema de Agendamiento Médico",
        default_version='v1',
        description="Documentación de la API para el Sistema de Agendamiento Médico",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
#Viewsets
router.register(r'pacientes', paciente_views.PacienteViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', lambda request: render(request, 'menu_principal.html'), name='menu_principal'),
    path('admin/', admin.site.urls),
    path('paciente/crear/', views.crear_paciente, name='crear_paciente'),
    path('paciente/', views.listar_pacientes, name='listar_pacientes'),
    path('paciente/eliminar/<int:pk>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('paciente/editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),

    path('empleado/crear/', empleado_views.crear_empleado, name='crear_empleado'),
    path('empleado/', empleado_views.listar_empleados, name='listar_empleados'),
    path('empleado/eliminar/<int:pk>/', empleado_views.eliminar_empleado, name='eliminar_empleado'),
    path('empleado/editar/<int:pk>/', empleado_views.editar_empleado, name='editar_empleado'),

    path('profesional/crear/', profesional_views.crear_profesional, name='crear_profesional'),
    path('profesional/', profesional_views.listar_profesionales, name='listar_profesionales'),
    path('profesional/eliminar/<int:pk>/', profesional_views.eliminar_profesional, name='eliminar_profesional'),
    path('profesional/editar/<int:pk>/', profesional_views.editar_profesional, name='editar_profesional'),
    path('profesional/<int:pk>/', profesional_views.detalle_profesional, name='detalle_profesional'),

    path('turno/crear/', turno_views.crear_turno, name='crear_turno'),
    path('turno/', turno_views.listar_turnos, name='listar_turnos'),
    path('turno/eliminar/<int:pk>/', turno_views.eliminar_turno, name='eliminar_turno'),
    path('turno/editar/<int:pk>/', turno_views.editar_turno, name='editar_turno'),
    path('turno/<int:pk>/resuelto/', turno_views.marcar_turno_resuelto, name='marcar_turno_resuelto'),
    path('turno/<int:pk>/cancelado/', turno_views.marcar_turno_cancelado, name='marcar_turno_cancelado'),

    path('disponibilidad/', profesional_views.listar_disponibilidades, name='listar_disponibilidades'),
    path('disponibilidad/crear/', profesional_views.crear_disponibilidad, name='crear_disponibilidad'),
    path('disponibilidad/editar/<int:pk>/', profesional_views.editar_disponibilidad, name='editar_disponibilidad'),
    path('disponibilidad/eliminar/<int:pk>/', profesional_views.eliminar_disponibilidad, name='eliminar_disponibilidad'),

    path('pacientes/historiales/', paciente_views.listar_historiales, name='listar_historiales'),
    path('pacientes/historiales/crear/', paciente_views.crear_historial, name='crear_historial'),
    path('pacientes/historiales/<int:pk>/editar/', paciente_views.editar_historial, name='editar_historial'),
    path('pacientes/historiales/<int:pk>/eliminar/', paciente_views.eliminar_historial, name='eliminar_historial'),
    path('pacientes/reportes/', paciente_views.listar_reportes, name='listar_reportes'),
    path('pacientes/reportes/crear/', paciente_views.crear_reporte, name='crear_reporte'),
    path('pacientes/reportes/<int:pk>/editar/', paciente_views.editar_reporte, name='editar_reporte'),
    path('pacientes/reportes/<int:pk>/eliminar/', paciente_views.eliminar_reporte, name='eliminar_reporte'),
]
