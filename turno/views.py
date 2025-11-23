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
from rest_framework import status
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


def _extract_validation_error_message(error):
    """Extrae el mensaje de error de una ValidationError."""
    if hasattr(error, 'message_dict'):
        return ' '.join([
            f"{field}: {', '.join(errors)}" 
            for field, errors in error.message_dict.items()
        ])
    if hasattr(error, 'messages'):
        return ' '.join(error.messages)
    return str(error)


def _extract_form_errors(form):
    """Extrae mensajes de error del formulario."""
    if form.errors:
        return ' '.join([
            f"{field}: {', '.join(errors)}" 
            for field, errors in form.errors.items()
        ])
    return ''


def _get_initial_paciente_data(request):
    """Obtiene datos iniciales del paciente para el formulario."""
    from paciente.models import Paciente
    
    initial_data = {}
    if request.user.groups.filter(name__iexact='pacientes').exists():
        if hasattr(request.user, 'paciente'):
            initial_data['paciente'] = request.user.paciente
        else:
            paciente = Paciente.objects.filter(ci=request.user.username).first()
            if paciente:
                initial_data['paciente'] = paciente
    return initial_data


@login_required
@permission_required('turno.add_turno', raise_exception=True)
def crear_turno(request):
    """
    Vista para crear un nuevo turno solo para el paciente autenticado, 
    filtrando profesionales por especialidad y validando disponibilidad.
    """
    from django.core.exceptions import ValidationError
    
    mensaje_error = ''
    
    if request.method == 'POST':
        form = TurnoForm(request.POST, request=request)
        if form.is_valid():
            try:
                turno = form.save(commit=False)
                turno.full_clean()
                turno.save()
                return redirect('listar_turnos')
            except ValidationError as e:
                mensaje_error = _extract_validation_error_message(e)
        else:
            mensaje_error = _extract_form_errors(form)
    else:
        initial_data = _get_initial_paciente_data(request)
        form = TurnoForm(initial=initial_data, request=request)
    
    return render(request, 'crear_turno.html', {
        'form': form, 
        'mensaje_error': mensaje_error
    })

def _get_paciente_from_user(user):
    """Obtiene el paciente asociado al usuario."""
    if hasattr(user, 'paciente'):
        return user.paciente
    from paciente.models import Paciente
    return Paciente.objects.filter(ci=user.username).first()

def _filter_turnos_by_estado(queryset, mostrar_ocultos):
    """Filtra turnos según el parámetro mostrar_ocultos."""
    if mostrar_ocultos:
        return queryset.filter(estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])
    return queryset.exclude(estado__in=[ESTADO_PENDIENTE, ESTADO_CANCELADO])

def _apply_search_query(queryset, query):
    """Aplica filtros de búsqueda al queryset de turnos."""
    if not query:
        return queryset
    return queryset.filter(
        Q(fecha__icontains=query) |
        Q(estado__icontains=query) |
        Q(profesional__nombre__icontains=query) |
        Q(profesional__apellido__icontains=query) |
        Q(paciente__nombre__icontains=query) |
        Q(paciente__apellido__icontains=query) |
        Q(empleado__nombre__icontains=query) |
        Q(empleado__apellido__icontains=query)
    )

@login_required
@permission_required('turno.view_turno', raise_exception=True)
def listar_turnos(request):
    """
    Vista para listar turnos. Si el usuario es del grupo 'pacientes', solo ve sus propios turnos.
    """
    mostrar_ocultos = request.GET.get('mostrar_ocultos', '') == '1'
    
    if request.user.groups.filter(name__iexact='pacientes').exists():
        paciente = _get_paciente_from_user(request.user)
        if paciente:
            turnos = _filter_turnos_by_estado(Turno.objects.filter(paciente=paciente), mostrar_ocultos)
        else:
            turnos = Turno.objects.none()
        return render(request, 'listar_turnos.html', {'turnos': turnos, 'q': '', 'mostrar_ocultos': mostrar_ocultos})
    
    query = request.GET.get('q', '')
    turnos = _filter_turnos_by_estado(Turno.objects.all(), mostrar_ocultos)
    turnos = _apply_search_query(turnos, query)
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
from .models import Turno, RecordatorioTurno
from .serializers import TurnoSerializer, RecordatorioTurnoSerializer

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

class RecordatorioTurnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar recordatorios de turnos.
    Permite listar, crear, actualizar y eliminar recordatorios.
    
    Filtros disponibles por query params:
    - turno: Filtrar por ID de turno
    - paciente: Filtrar por ID de paciente
    - enviado: Filtrar por estado de envío (true/false)
    """
    queryset = RecordatorioTurno.objects.all()
    serializer_class = RecordatorioTurnoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['turno', 'paciente', 'enviado']

