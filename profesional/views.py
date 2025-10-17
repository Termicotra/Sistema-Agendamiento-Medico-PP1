from django.shortcuts import render, redirect
from django.db.models import Q
from profesional.forms import ProfesionalForm, DisponibilidadForm
from profesional.models import Profesional, Disponibilidad

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

def eliminar_profesional(request, pk):
    """
    Vista para eliminar un profesional específico.
    """
    profesional = Profesional.objects.get(pk=pk)
    if request.method == 'POST':
        profesional.delete()
        return redirect('listar_profesionales')
    return render(request, 'eliminar_profesional.html', {'profesional': profesional})

def editar_profesional(request, pk):
    """
    Vista para editar los datos de un profesional existente.
    """
    profesional = Profesional.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            return redirect('listar_profesionales')
    else:
        form = ProfesionalForm(instance=profesional)
    return render(request, 'editar_profesional.html', {'form': form, 'profesional': profesional})

def detalle_profesional(request, pk):
    """
    Vista para mostrar el detalle de un profesional específico.
    """
    profesional = Profesional.objects.get(pk=pk)
    disponibilidades = Disponibilidad.objects.filter(profesional=profesional)
    return render(request, 'detalle_profesional.html', {
        'profesional': profesional,
        'disponibilidades': disponibilidades
    })

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

def crear_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_disponibilidades')
    else:
        form = DisponibilidadForm()
    return render(request, 'crear_disponibilidad.html', {'form': form})

def editar_disponibilidad(request, pk):
    disponibilidad = Disponibilidad.objects.get(pk=pk)
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('listar_disponibilidades')
    else:
        form = DisponibilidadForm(instance=disponibilidad)
    return render(request, 'editar_disponibilidad.html', {'form': form, 'disponibilidad': disponibilidad})

def eliminar_disponibilidad(request, pk):
    disponibilidad = Disponibilidad.objects.get(pk=pk)
    if request.method == 'POST':
        disponibilidad.delete()
        return redirect('listar_disponibilidades')
    return render(request, 'eliminar_disponibilidad.html', {'disponibilidad': disponibilidad})

from rest_framework import viewsets
from .models import Profesional
from .models import Disponibilidad
from .serializers import ProfesionalSerializer
from .serializers import DisponibilidadSerializer

class ProfesionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar profesionales.
    Permite listar, crear, actualizar y eliminar profesionales del sistema de agendamiento.
    """
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer

class DisponibilidadViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar disponibilidades de los profesionales.
    Permite listar, crear, actualizar y eliminar disponibilidades.
    """
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
