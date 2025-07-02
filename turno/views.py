from django.shortcuts import render, redirect
from django.db.models import Q
from turno.models import Turno
from turno.forms import TurnoForm

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
    turnos = Turno.objects.all()
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
    return render(request, 'listar_turnos.html', {'turnos': turnos, 'q': query})

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
