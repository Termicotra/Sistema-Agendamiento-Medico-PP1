from django.shortcuts import render
from paciente.models import Paciente, HistorialClinico, ReporteMedico
from paciente.forms import PacienteForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')  
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

def listar_pacientes(request):
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    if query:
        pacientes = pacientes.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(ci__icontains=query)
        )
    return render(request, 'listar_pacientes.html', {'pacientes': pacientes, 'q': query})

def eliminar_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

def editar_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})

def listar_historiales(request):
    query = request.GET.get('q', '')
    historiales = HistorialClinico.objects.select_related('paciente', 'profesional').all()
    if query:
        historiales = historiales.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(profesional__nombre__icontains=query) |
            Q(profesional__apellido__icontains=query) |
            Q(fecha__icontains=query)
        )
    return render(request, 'listar_historiales.html', {'historiales': historiales, 'q': query})

def crear_historial(request):
    from paciente.forms import HistorialClinicoForm
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_historiales')
    else:
        form = HistorialClinicoForm()
    return render(request, 'crear_historial.html', {'form': form})

def editar_historial(request, pk):
    from paciente.forms import HistorialClinicoForm
    historial = HistorialClinico.objects.get(pk=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('listar_historiales')
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'editar_historial.html', {'form': form, 'historial': historial})

def eliminar_historial(request, pk):
    historial = HistorialClinico.objects.get(pk=pk)
    if request.method == 'POST':
        historial.delete()
        return redirect('listar_historiales')
    return render(request, 'eliminar_historial.html', {'historial': historial})

def listar_reportes(request):
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

def crear_reporte(request):
    from paciente.forms import ReporteMedicoForm
    if request.method == 'POST':
        form = ReporteMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reportes')
    else:
        form = ReporteMedicoForm()
    return render(request, 'crear_reporte.html', {'form': form})

def editar_reporte(request, pk):
    from paciente.forms import ReporteMedicoForm
    reporte = ReporteMedico.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReporteMedicoForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('listar_reportes')
    else:
        form = ReporteMedicoForm(instance=reporte)
    return render(request, 'editar_reporte.html', {'form': form, 'reporte': reporte})

def eliminar_reporte(request, pk):
    reporte = ReporteMedico.objects.get(pk=pk)
    if request.method == 'POST':
        reporte.delete()
        return redirect('listar_reportes')
    return render(request, 'eliminar_reporte.html', {'reporte': reporte})
