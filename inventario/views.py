from django.shortcuts import render, redirect
from django.db.models import Q
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
    query = request.GET.get('q', '')
    insumos = Insumo.objects.all()
    if query:
        insumos = insumos.filter(
            Q(nombre__icontains=query) |
            Q(laboratorio__icontains=query) |
            Q(fecha_caducidad__icontains=query)
        )
    return render(request, 'listar_insumos.html', {'insumos': insumos, 'q': query})

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
