from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from profesional.forms import ProfesionalForm, DisponibilidadForm
from profesional.models import Profesional, Disponibilidad
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import ProfesionalSerializer, DisponibilidadSerializer
from rest_framework.permissions import DjangoModelPermissions

@login_required
@permission_required('profesional.add_profesional', raise_exception=True)
def crear_profesional(request):
    """
    Vista para crear un nuevo profesional mediante un formulario web.
    """
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_profesionales')
    else:
        form = ProfesionalForm()
    return render(request, 'crear_profesional.html', {'form': form})

@login_required
@permission_required('profesional.view_profesional', raise_exception=True)
def listar_profesionales(request):
    """
    Vista para listar y buscar profesionales registrados en el sistema.
    """
    query = request.GET.get('q', '')
    profesionales = Profesional.objects.all()
    if query:
        profesionales = profesionales.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(especialidad__icontains=query) |
            Q(ci__icontains=query)
        )
    return render(request, 'listar_profesionales.html', {'profesionales': profesionales, 'q': query})

@login_required
@permission_required('profesional.delete_profesional', raise_exception=True)
def eliminar_profesional(request, pk):
    """
    Vista para eliminar un profesional específico.
    """
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        profesional.delete()
        return redirect('listar_profesionales')
    return render(request, 'eliminar_profesional.html', {'profesional': profesional})

@login_required
@permission_required('profesional.change_profesional', raise_exception=True)
def editar_profesional(request, pk):
    """
    Vista para editar los datos de un profesional existente.
    """
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            return redirect('listar_profesionales')
    else:
        form = ProfesionalForm(instance=profesional)
    return render(request, 'editar_profesional.html', {'form': form, 'profesional': profesional})

@login_required
@permission_required('profesional.view_profesional', raise_exception=True)
def detalle_profesional(request, pk):
    """
    Vista para mostrar el detalle de un profesional específico.
    """
    profesional = get_object_or_404(Profesional, pk=pk)
    disponibilidades = Disponibilidad.objects.filter(profesional=profesional)
    return render(request, 'detalle_profesional.html', {
        'profesional': profesional,
        'disponibilidades': disponibilidades
    })

@login_required
@permission_required('profesional.view_disponibilidad', raise_exception=True)
def listar_disponibilidades(request):
    profesional_id = request.GET.get('profesional')
    disponibilidades = Disponibilidad.objects.select_related('profesional').all()
    profesional_filtrado = None
    if profesional_id:
        disponibilidades = disponibilidades.filter(profesional_id=profesional_id)
        try:
            profesional_filtrado = Profesional.objects.get(pk=profesional_id)
        except Profesional.DoesNotExist:
            profesional_filtrado = None
    return render(request, 'listar_disponibilidades.html', {
        'disponibilidades': disponibilidades,
        'profesional_filtrado': profesional_filtrado
    })

@login_required
@permission_required('profesional.add_disponibilidad', raise_exception=True)
def crear_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_disponibilidades')
    else:
        form = DisponibilidadForm()
    return render(request, 'crear_disponibilidad.html', {'form': form})

@login_required
@permission_required('profesional.change_disponibilidad', raise_exception=True)
def editar_disponibilidad(request, pk):
    disponibilidad = get_object_or_404(Disponibilidad, pk=pk)
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('listar_disponibilidades')
    else:
        form = DisponibilidadForm(instance=disponibilidad)
    return render(request, 'editar_disponibilidad.html', {'form': form, 'disponibilidad': disponibilidad})

@login_required
@permission_required('profesional.delete_disponibilidad', raise_exception=True)
def eliminar_disponibilidad(request, pk):
    disponibilidad = get_object_or_404(Disponibilidad, pk=pk)
    if request.method == 'POST':
        disponibilidad.delete()
        return redirect('listar_disponibilidades')
    return render(request, 'eliminar_disponibilidad.html', {'disponibilidad': disponibilidad})


class ProfesionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar profesionales.
    Permite listar, crear, actualizar y eliminar profesionales del sistema.
    """
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    permission_classes = [DjangoModelPermissions]

class DisponibilidadViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar disponibilidades de los profesionales.
    Permite listar, crear, actualizar y eliminar disponibilidades.
    """
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Disponibilidad.objects.all()
        profesional_id = self.request.query_params.get('profesional')
        if profesional_id:
            queryset = queryset.filter(profesional_id=profesional_id)
        return queryset
