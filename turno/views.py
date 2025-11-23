from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from turno.models import Turno
from turno.forms import TurnoForm
from rest_framework import viewsets
from .serializers import TurnoSerializer
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Constantes de estado
ESTADO_PENDIENTE = 'Pendiente'
ESTADO_ACTIVO = 'Activo'
ESTADO_COMPLETADO = 'Completado'
ESTADO_CANCELADO = 'Cancelado'

# Constantes de estado
ESTADO_PENDIENTE = 'Pendiente'
ESTADO_ACTIVO = 'Activo'
ESTADO_COMPLETADO = 'Completado'
ESTADO_CANCELADO = 'Cancelado'

@login_required
@permission_required('turno.view_turno', raise_exception=True)
def solicitudes_turno(request):
    """Vista para el módulo de solicitudes de turno (pendientes) solo para administradores."""
    turnos = Turno.objects.filter(estado=ESTADO_PENDIENTE)
    return render(request, 'solicitudes_turno.html', {'turnos': turnos})

@login_required
@permission_required('turno.change_turno', raise_exception=True)
@csrf_exempt
def marcar_turno_activo(request, pk):
    """Permite marcar un turno pendiente como activo desde la vista de solicitudes."""
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST' and turno.estado == ESTADO_PENDIENTE:
        turno.estado = ESTADO_ACTIVO
        turno.save()
    return redirect('solicitudes_turno')

@login_required
@permission_required('turno.add_turno', raise_exception=True)
def crear_turno(request):
    """
    Vista para crear un nuevo turno solo para el paciente autenticado, 
    filtrando profesionales por especialidad y validando disponibilidad.
    """
    from paciente.models import Paciente
    from django.core.exceptions import ValidationError
    
    mensaje_error = ''
    
    if request.method == 'POST':
        form = TurnoForm(request.POST, request=request)
        if form.is_valid():
            try:
                turno = form.save(commit=False)
                turno.full_clean()  # Ejecuta validaciones del modelo
                turno.save()
                return redirect('listar_turnos')
            except ValidationError as e:
                # Extraer mensajes de error de ValidationError
                if hasattr(e, 'message_dict'):
                    mensaje_error = ' '.join([
                        f"{field}: {', '.join(errors)}" 
                        for field, errors in e.message_dict.items()
                    ])
                elif hasattr(e, 'messages'):
                    mensaje_error = ' '.join(e.messages)
                else:
                    mensaje_error = str(e)
        else:
            # Capturar errores de validación del formulario
            if form.errors:
                mensaje_error = ' '.join([
                    f"{field}: {', '.join(errors)}" 
                    for field, errors in form.errors.items()
                ])
    else:
        # Si el usuario es paciente, pre-seleccionar su paciente
        initial_data = {}
        if request.user.groups.filter(name__iexact='pacientes').exists():
            if hasattr(request.user, 'paciente'):
                initial_data['paciente'] = request.user.paciente
            else:
                paciente = Paciente.objects.filter(ci=request.user.username).first()
                if paciente:
                    initial_data['paciente'] = paciente
        
        form = TurnoForm(initial=initial_data, request=request)
    
    return render(request, 'crear_turno.html', {
        'form': form, 
        'mensaje_error': mensaje_error
    })

@login_required
@permission_required('turno.view_turno', raise_exception=True)
def listar_turnos(request):
    """
    Vista para listar turnos. Si el usuario es del grupo 'pacientes', solo ve sus propios turnos.
    """
    mostrar_ocultos = request.GET.get('mostrar_ocultos', '') == '1'
    if request.user.groups.filter(name__iexact='pacientes').exists():
        if hasattr(request.user, 'paciente'):
            paciente = request.user.paciente
        else:
            from paciente.models import Paciente
            paciente = Paciente.objects.filter(ci=request.user.username).first()
        if paciente:
            if mostrar_ocultos:
                turnos = Turno.objects.filter(paciente=paciente, estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])
            else:
                turnos = Turno.objects.filter(paciente=paciente).exclude(estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])
        else:
            turnos = Turno.objects.none()
        return render(request, 'listar_turnos.html', {'turnos': turnos, 'q': '', 'mostrar_ocultos': mostrar_ocultos})
    else:
        query = request.GET.get('q', '')
        if mostrar_ocultos:
            turnos = Turno.objects.filter(estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])
        else:
            turnos = Turno.objects.exclude(estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])
        if query:
            turnos = turnos.filter(
                Q(fecha__icontains=query) |
                Q(estado__icontains=query) |
                Q(profesional__nombre__icontains=query) |
                Q(profesional__apellido__icontains=query) |
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(empleado__nombre__icontains=query) |
                Q(empleado__apellido__icontains=query)
            )
        return render(request, 'listar_turnos.html', {'turnos': turnos, 'q': query, 'mostrar_ocultos': mostrar_ocultos})

@login_required
@permission_required('turno.delete_turno', raise_exception=True)
def eliminar_turno(request, pk):
    """
    Vista para eliminar un turno específico.
    """
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.delete()
        return redirect('listar_turnos')
    return render(request, 'eliminar_turno.html', {'turno': turno})

@login_required
@permission_required('turno.change_turno', raise_exception=True)
def editar_turno(request, pk):
    """
    Vista para editar los datos de un turno existente.
    """
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'editar_turno.html', {'form': form, 'turno': turno})

@login_required
@permission_required('turno.change_turno', raise_exception=True)
def marcar_turno_resuelto(request, pk):
    """
    Vista para marcar un turno como resuelto.
    """
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.estado = ESTADO_COMPLETADO
        turno.save()
    return redirect('listar_turnos')

@login_required
@permission_required('turno.change_turno', raise_exception=True)
def marcar_turno_cancelado(request, pk):
    """
    Vista para marcar un turno como cancelado.
    """
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.estado = ESTADO_CANCELADO
        turno.save()
        return redirect('listar_turnos')
    # Si no es POST, mostrar confirmación
    return render(request, 'cancelar_turno.html', {'turno': turno})

from rest_framework import viewsets
from .models import Turno
from .models import RecordatorioTurno
from .serializers import TurnoSerializer
from .serializers import RecordatorioTurnoSerializer

from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend

class TurnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar turnos.
    Permite listar, crear, actualizar y eliminar turnos del sistema.
    
    Filtros disponibles por query params:
    - estado: Filtrar por estado (Pendiente, Activo, Completado, Cancelado)
    - profesional: Filtrar por ID de profesional
    - paciente: Filtrar por ID de paciente
    - fecha: Filtrar por fecha exacta
    
    Ejemplos:
    - GET /api/turnos/?estado=Pendiente
    - GET /api/turnos/?profesional=1&estado=Activo
    - GET /api/turnos/?paciente=5
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'profesional', 'paciente', 'fecha', 'modalidad']

