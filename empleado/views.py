from django.shortcuts import render, redirect
from django.db.models import Q
from empleado.models import Empleado
from empleado.forms import EmpleadoForm

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'crear_empleado.html', {'form': form})

def listar_empleados(request):
    query = request.GET.get('q', '')
    empleados = Empleado.objects.all()
    if query:
        empleados = empleados.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(ci__icontains=query) |
            Q(cargo__icontains=query)
        )
    return render(request, 'listar_empleados.html', {'empleados': empleados, 'q': query})

def eliminar_empleado(request, pk):
    empleado = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('listar_empleados')
    return render(request, 'eliminar_empleado.html', {'empleado': empleado})

def editar_empleado(request, pk):
    empleado = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'editar_empleado.html', {'form': form, 'empleado': empleado})
