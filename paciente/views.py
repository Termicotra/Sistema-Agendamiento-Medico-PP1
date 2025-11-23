from django.shortcuts import render, redirect, get_object_or_404
from paciente.models import Paciente, HistorialClinico, ReporteMedico
from paciente.forms import PacienteForm, HistorialClinicoForm, ReporteMedicoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from rest_framework import viewsets
from .serializers import PacienteSerializer, HistorialClinicoSerializer, ReporteMedicoSerializer
from .filters import PacienteFilter, HistorialClinicoFilter
from django_filters.rest_framework import DjangoFilterBackend

def _get_paciente_for_user(user):
    """Obtiene el paciente asociado al usuario actual."""
    if hasattr(user, 'paciente'):
        return [user.paciente]
    return list(Paciente.objects.filter(ci=user.username)[:1])

def _get_historiales_for_user(user):
    """Obtiene historiales del paciente asociado al usuario."""
    if hasattr(user, 'paciente'):
        return HistorialClinico.objects.filter(paciente=user.paciente)
    return HistorialClinico.objects.filter(paciente__ci=user.username)

def _build_paciente_filters(query):
    """Construye filtros de búsqueda para pacientes."""
    partes = query.replace('+', ' ').split()
    
    if len(partes) == 1 and partes[0].isdigit():
        return Q(ci__icontains=partes[0])
    
    if len(partes) > 1:
        filtros = Q()
        for parte in partes:
            if parte.isdigit():
                filtros |= Q(ci__icontains=parte)
            else:
                filtros |= Q(nombre__icontains=parte) | Q(apellido__icontains=parte)
        return filtros
    
    return Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(ci__icontains=query)

def _build_historial_filters(query):
    """Construye filtros de búsqueda para historiales clínicos."""
    partes = query.replace('+', ' ').split()
    
    if len(partes) == 1 and partes[0].isdigit():
        return Q(paciente__ci__icontains=partes[0])
    
    if len(partes) > 1:
        filtros = Q()
        for parte in partes:
            if parte.isdigit():
                filtros |= Q(paciente__ci__icontains=parte)
            else:
                filtros |= Q(paciente__nombre__icontains=parte) | Q(paciente__apellido__icontains=parte)
        return filtros
    
    return (Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(paciente__ci__icontains=query) |
            Q(profesional__nombre__icontains=query) |
            Q(profesional__apellido__icontains=query) |
            Q(fecha__icontains=query))

@login_required
@permission_required('paciente.add_paciente', raise_exception=True)
def crear_paciente(request):
    """
    Vista para crear un nuevo paciente mediante un formulario web.
    """
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')  
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

@login_required
@permission_required('paciente.view_paciente', raise_exception=True)
def listar_pacientes(request):
    """
    Vista para listar pacientes. Si el usuario es del grupo 'Pacientes', solo ve su propio perfil.
    """
    if request.user.groups.filter(name='Pacientes').exists():
        pacientes = _get_paciente_for_user(request.user)
        return render(request, 'listar_pacientes.html', {'pacientes': pacientes, 'q': ''})
    
    query = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.all()
    if query:
        pacientes = pacientes.filter(_build_paciente_filters(query))
    return render(request, 'listar_pacientes.html', {'pacientes': pacientes, 'q': query})

@login_required
@permission_required('paciente.delete_paciente', raise_exception=True)
def eliminar_paciente(request, pk):
    """
    Vista para eliminar un paciente específico.
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

@login_required
@permission_required('paciente.change_paciente', raise_exception=True)
def editar_paciente(request, pk):
    """
    Vista para editar los datos de un paciente existente.
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})

@login_required
@permission_required('paciente.view_historialclinico', raise_exception=True)
def listar_historiales(request):
    """
    Vista para listar historiales. Si el usuario es del grupo 'Pacientes', solo ve sus propios historiales.
    """
    if request.user.groups.filter(name='Pacientes').exists():
        historiales = _get_historiales_for_user(request.user)
        return render(request, 'listar_historiales.html', {'historiales': historiales, 'q': ''})
    
    query = request.GET.get('q', '').strip()
    historiales = HistorialClinico.objects.select_related('paciente', 'profesional').all()
    if query:
        historiales = historiales.filter(_build_historial_filters(query))
    return render(request, 'listar_historiales.html', {'historiales': historiales, 'q': query})

@login_required
@permission_required('paciente.add_historialclinico', raise_exception=True)
def crear_historial(request):
    """
    Vista para crear un nuevo historial clínico para un paciente.
    """
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_historiales')
    else:
        form = HistorialClinicoForm()
    return render(request, 'crear_historial.html', {'form': form})

@login_required
@permission_required('paciente.change_historialclinico', raise_exception=True)
def editar_historial(request, pk):
    """
    Vista para editar un historial clínico existente.
    """
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('listar_historiales')
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'editar_historial.html', {'form': form, 'historial': historial})

@login_required
@permission_required('paciente.delete_historialclinico', raise_exception=True)
def eliminar_historial(request, pk):
    """
    Vista para eliminar un historial clínico específico.
    """
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        historial.delete()
        return redirect('listar_historiales')
    return render(request, 'eliminar_historial.html', {'historial': historial})

@login_required
@permission_required('paciente.view_reportemedico', raise_exception=True)
def listar_reportes(request):
    """
    Vista para listar y buscar reportes médicos de pacientes.
    """
    query = request.GET.get('q', '')
    reportes = ReporteMedico.objects.select_related('paciente', 'profesional').all()
    if query:
        reportes = reportes.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(profesional__nombre__icontains=query) |
            Q(profesional__apellido__icontains=query) |
            Q(fecha__icontains=query)
        )
    return render(request, 'listar_reportes.html', {'reportes': reportes, 'q': query})

@login_required
@permission_required('paciente.add_reportemedico', raise_exception=True)
def crear_reporte(request):
    """
    Vista para crear un nuevo reporte médico para un paciente.
    """
    if request.method == 'POST':
        form = ReporteMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reportes')
    else:
        form = ReporteMedicoForm()
    return render(request, 'crear_reporte.html', {'form': form})

@login_required
@permission_required('paciente.change_reportemedico', raise_exception=True)
def editar_reporte(request, pk):
    """
    Vista para editar un reporte médico existente.
    """
    reporte = get_object_or_404(ReporteMedico, pk=pk)
    if request.method == 'POST':
        form = ReporteMedicoForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('listar_reportes')
    else:
        form = ReporteMedicoForm(instance=reporte)
    return render(request, 'editar_reporte.html', {'form': form, 'reporte': reporte})

@login_required
@permission_required('paciente.delete_reportemedico', raise_exception=True)
def eliminar_reporte(request, pk):
    """
    Vista para eliminar un reporte médico específico.
    """
    reporte = get_object_or_404(ReporteMedico, pk=pk)
    if request.method == 'POST':
        reporte.delete()
        return redirect('listar_reportes')
    return render(request, 'eliminar_reporte.html', {'reporte': reporte})

def listar_reportes_medicos(request):
    """
    Vista para listar y buscar reportes médicos con filtros avanzados.
    """
    query = request.GET.get('q', '').strip()
    reportes = ReporteMedico.objects.select_related('paciente', 'profesional').all()
    if query:
        partes = query.replace('+', ' ').split()
        # Si el query es solo un CI (todo numérico)
        if len(partes) == 1 and partes[0].isdigit():
            reportes = reportes.filter(paciente__ci__icontains=partes[0])
        elif len(partes) > 1:
            filtros = Q()
            for parte in partes:
                if parte.isdigit():
                    filtros |= Q(paciente__ci__icontains=parte)
                else:
                    filtros |= Q(paciente__nombre__icontains=parte) | Q(paciente__apellido__icontains=parte)
            reportes = reportes.filter(filtros)
        else:
            reportes = reportes.filter(
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(paciente__ci__icontains=query) |
                Q(profesional__nombre__icontains=query) |
                Q(profesional__apellido__icontains=query) |
                Q(fecha__icontains=query)
            )
    return render(request, 'listar_reportes_medicos.html', {'reportes': reportes, 'q': query})



class PacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar pacientes.
    Permite listar, crear, actualizar y eliminar pacientes del sistema de agendamiento.
    """
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PacienteFilter

class HistorialClinicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar historiales clínicos.
    Permite listar, crear, actualizar y eliminar historiales clínicos asociados a pacientes.
    """
    queryset = HistorialClinico.objects.all()
    serializer_class = HistorialClinicoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistorialClinicoFilter

class ReporteMedicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar reportes médicos.
    Permite listar, crear, actualizar y eliminar reportes médicos asociados a pacientes.
    """
    queryset = ReporteMedico.objects.all()
    serializer_class = ReporteMedicoSerializer
