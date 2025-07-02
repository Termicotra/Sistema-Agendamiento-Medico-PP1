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
