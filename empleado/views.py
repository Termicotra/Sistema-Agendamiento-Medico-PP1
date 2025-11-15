from django.shortcuts import render, redirect
from django.db.models import Q
from empleado.models import Empleado
from empleado.forms import EmpleadoForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('empleado.add_empleado', raise_exception=True)
def crear_empleado(request):
    """
    Vista para crear un nuevo empleado mediante un formulario web.
    """
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'crear_empleado.html', {'form': form})

@login_required
@permission_required('empleado.view_empleado', raise_exception=True)
def listar_empleados(request):
    """
    Vista para listar y buscar empleados registrados en el sistema.
    """
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

@login_required
@permission_required('empleado.delete_empleado', raise_exception=True)
def eliminar_empleado(request, pk):
    """
    Vista para eliminar un empleado específico.
    """
    empleado = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('listar_empleados')
    return render(request, 'eliminar_empleado.html', {'empleado': empleado})

@login_required
@permission_required('empleado.change_empleado', raise_exception=True)
def editar_empleado(request, pk):
    """
    Vista para editar los datos de un empleado existente.
    """
    empleado = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'editar_empleado.html', {'form': form, 'empleado': empleado})


from rest_framework import viewsets
from .models import Empleado
from .serializers import EmpleadoSerializer

from rest_framework.permissions import DjangoModelPermissions

class EmpleadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar empleados.
    Permite listar, crear, actualizar y eliminar empleados del sistema.
    """
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [DjangoModelPermissions]
