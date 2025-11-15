from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST
from turno.models import Turno
from turno.forms import TurnoForm
from django.contrib.auth.decorators import login_required, permission_required

RESUELTO = 'No activo'
CANCELADO = 'Cancelado'

@login_required
@permission_required('turno.add_turno', raise_exception=True)
def crear_turno(request):
    """
    Vista para crear un nuevo turno solo para el paciente autenticado, filtrando profesionales por especialidad y validando disponibilidad.
    """
    from paciente.models import Paciente
    from profesional.models import Profesional, Disponibilidad
    mensaje_error = ''
    disponibilidades = []
    if hasattr(request.user, 'paciente'):
        paciente = request.user.paciente

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
                turnos = Turno.objects.filter(paciente=paciente, estado__in=[RESUELTO, CANCELADO])
            else:
                turnos = Turno.objects.filter(paciente=paciente).exclude(estado__in=[RESUELTO, CANCELADO])
        else:
            turnos = Turno.objects.none()
        return render(request, 'listar_turnos.html', {'turnos': turnos, 'q': '', 'mostrar_ocultos': mostrar_ocultos})
    else:
        query = request.GET.get('q', '')
        if mostrar_ocultos:
            turnos = Turno.objects.filter(estado__in=[RESUELTO, CANCELADO])
        else:
            turnos = Turno.objects.exclude(estado__in=[RESUELTO, CANCELADO])
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
    turno = Turno.objects.get(pk=pk)
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
    turno = Turno.objects.get(pk=pk)
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
        turno.estado = RESUELTO
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
        turno.estado = 'Cancelado'
        turno.save()
        return redirect('listar_turnos')
    # Si no es POST, mostrar confirmación
    return render(request, 'cancelar_turno.html', {'turno': turno})

from rest_framework import viewsets
from .models import Turno
from .serializers import TurnoSerializer

from rest_framework.permissions import DjangoModelPermissions

class TurnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar turnos.
    Permite listar, crear, actualizar y eliminar turnos del sistema.
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [DjangoModelPermissions]