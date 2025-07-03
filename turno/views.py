from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST
from turno.models import Turno
from turno.forms import TurnoForm
from facturacion.models import Facturacion

def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm()
    return render(request, 'crear_turno.html', {'form': form})

def listar_turnos(request):
    query = request.GET.get('q', '')
    mostrar_ocultos = request.GET.get('mostrar_ocultos', '') == '1'
    if mostrar_ocultos:
        turnos = Turno.objects.filter(estado__in=['No activo', 'Cancelado'])
    else:
        turnos = Turno.objects.exclude(estado__in=['No activo', 'Cancelado'])
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
    turno = Turno.objects.get(pk=pk)
    if request.method == 'POST':
        turno.delete()
        return redirect('listar_turnos')
    return render(request, 'eliminar_turno.html', {'turno': turno})

def editar_turno(request, pk):
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
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.estado = 'No activo'
        turno.save()
    return redirect('listar_turnos')

def marcar_turno_cancelado(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        turno.estado = 'Cancelado'
        turno.save()
        # Anular automáticamente la facturación asociada si existe y está pendiente
        facturaciones = Facturacion.objects.filter(turno=turno, estado=Facturacion.EstadoFacturacionChoices.PENDIENTE)
        for facturacion in facturaciones:
            facturacion.estado = Facturacion.EstadoFacturacionChoices.ANULADO
            facturacion.save()
        return redirect('listar_turnos')
    # Si no es POST, mostrar confirmación
    return render(request, 'cancelar_turno.html', {'turno': turno})
