from django.shortcuts import render, redirect
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
    turnos = Turno.objects.all()
    return render(request, 'listar_turnos.html', {'turnos': turnos})

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
