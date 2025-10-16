from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST
from turno.models import Turno
from turno.forms import TurnoForm

RESUELTO = 'No activo'
CANCELADO = 'Cancelado'

def crear_turno(request):
    """
    Vista para crear un nuevo turno mediante un formulario web.
    """
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm()
    return render(request, 'crear_turno.html', {'form': form})

def listar_turnos(request):
    """
    Vista para listar y buscar turnos registrados en el sistema.
    """
    query = request.GET.get('q', '')
    mostrar_ocultos = request.GET.get('mostrar_ocultos', '') == '1'
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

def eliminar_turno(request, pk):
    """
    Vista para eliminar un turno específico.
    """
    turno = Turno.objects.get(pk=pk)
    if request.method == 'POST':
        turno.delete()
        return redirect('listar_turnos')
    return render(request, 'eliminar_turno.html', {'turno': turno})

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

def marcar_turno_resuelto(request, pk):
    """
    Vista para marcar un turno como resuelto.
    """
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.estado = RESUELTO
        turno.save()
    return redirect('listar_turnos')

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

class TurnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar turnos.
    Permite listar, crear, actualizar y eliminar turnos del sistema.
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer