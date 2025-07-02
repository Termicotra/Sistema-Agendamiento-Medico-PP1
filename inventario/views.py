from django.shortcuts import render, redirect
from inventario.models import Insumo
from inventario.forms import InsumoForm

def crear_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_insumos')
    else:
        form = InsumoForm()
    return render(request, 'crear_insumo.html', {'form': form})

def listar_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'listar_insumos.html', {'insumos': insumos})

def eliminar_insumo(request, pk):
    insumo = Insumo.objects.get(pk=pk)
    if request.method == 'POST':
        insumo.delete()
        return redirect('listar_insumos')
    return render(request, 'eliminar_insumo.html', {'insumo': insumo})

def editar_insumo(request, pk):
    insumo = Insumo.objects.get(pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            return redirect('listar_insumos')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'editar_insumo.html', {'form': form, 'insumo': insumo})
