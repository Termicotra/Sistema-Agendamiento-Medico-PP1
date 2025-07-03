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
    query = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.all()
    if query:
        partes = query.replace('+', ' ').split()
        # Si el query es solo un CI (todo numérico)
        if len(partes) == 1 and partes[0].isdigit():
            pacientes = pacientes.filter(ci__icontains=partes[0])
        elif len(partes) > 1:
            filtros = Q()
            for parte in partes:
                if parte.isdigit():
                    filtros |= Q(ci__icontains=parte)
                else:
                    filtros |= Q(nombre__icontains=parte) | Q(apellido__icontains=parte)
            pacientes = pacientes.filter(filtros)
        else:
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
    query = request.GET.get('q', '').strip()
    historiales = HistorialClinico.objects.select_related('paciente', 'profesional').all()
    if query:
        partes = query.replace('+', ' ').split()
        # Si el query es solo un CI (todo numérico)
        if len(partes) == 1 and partes[0].isdigit():
            historiales = historiales.filter(paciente__ci__icontains=partes[0])
        # Si el query tiene más de una palabra, buscar cada palabra en nombre o apellido (OR)
        elif len(partes) > 1:
            filtros = Q()
            for parte in partes:
                if parte.isdigit():
                    filtros |= Q(paciente__ci__icontains=parte)
                else:
                    filtros |= Q(paciente__nombre__icontains=parte) | Q(paciente__apellido__icontains=parte)
            historiales = historiales.filter(filtros)
        # Si es una sola palabra, buscar en nombre, apellido y ci (OR)
        else:
            historiales = historiales.filter(
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(paciente__ci__icontains=query) |
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

def listar_reportes_medicos(request):
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
