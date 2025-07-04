from django.shortcuts import render, redirect
from django.db.models import Q
from facturacion.models import Facturacion, DetalleFactura
from facturacion.forms import FacturacionForm, DetalleFacturaForm

def crear_facturacion(request):
    if request.method == 'POST':
        form = FacturacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_facturaciones')
    else:
        form = FacturacionForm()
    return render(request, 'crear_facturacion.html', {'form': form})

def listar_facturaciones(request):
    query = request.GET.get('q', '')
    mostrar_ocultos = request.GET.get('mostrar_ocultos', '') == '1'
    if mostrar_ocultos:
        facturaciones = Facturacion.objects.filter(estado__in=['Pagado', 'Anulado'])
    else:
        facturaciones = Facturacion.objects.filter(estado='Pendiente')
    if query:
        facturaciones = facturaciones.filter(
            Q(fecha__icontains=query) |
            Q(estado__icontains=query) |
            Q(metodo_pago__icontains=query) |
            Q(turno__id_turno__icontains=query) |
            Q(tipo_facturacion__icontains=query)
        )
    return render(request, 'listar_facturaciones.html', {'facturaciones': facturaciones, 'q': query, 'mostrar_ocultos': mostrar_ocultos})

def eliminar_facturacion(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    if request.method == 'POST':
        facturacion.delete()
        return redirect('listar_facturaciones')
    return render(request, 'eliminar_facturacion.html', {'facturacion': facturacion})

def editar_facturacion(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    if request.method == 'POST':
        form = FacturacionForm(request.POST, instance=facturacion)
        if form.is_valid():
            form.save()
            return redirect('listar_facturaciones')
    else:
        form = FacturacionForm(instance=facturacion)
    return render(request, 'editar_facturacion.html', {'form': form, 'facturacion': facturacion})

def detalle_facturacion(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    detalles = DetalleFactura.objects.filter(factura=facturacion)
    if request.method == 'POST':
        detalle_form = DetalleFacturaForm(request.POST)
        if detalle_form.is_valid():
            nuevo_detalle = detalle_form.save(commit=False)
            nuevo_detalle.factura = facturacion
            nuevo_detalle.save()
            return redirect('detalle_facturacion', pk=facturacion.pk)
    else:
        detalle_form = DetalleFacturaForm()
    return render(request, 'detalle_facturacion.html', {
        'facturacion': facturacion,
        'detalles': detalles,
        'detalle_form': detalle_form
    })

def eliminar_detalle_factura(request, detalle_pk):
    detalle = DetalleFactura.objects.get(pk=detalle_pk)
    facturacion_pk = detalle.factura.pk
    if request.method == 'POST':
        detalle.delete()
        return redirect('detalle_facturacion', pk=facturacion_pk)
    return render(request, 'eliminar_detalle_factura.html', {'detalle': detalle})

def marcar_facturacion_pagada(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    if request.method == 'POST':
        facturacion.estado = 'Pagado'
        facturacion.save()
        return redirect('listar_facturaciones')
    return redirect('listar_facturaciones')

def marcar_facturacion_anulada(request, pk):
    facturacion = Facturacion.objects.get(pk=pk)
    if request.method == 'POST':
        # Si el turno asociado está cancelado, anular la facturación automáticamente
        if facturacion.turno and facturacion.turno.estado == 'Cancelado':
            facturacion.estado = 'Anulado'
            facturacion.save()
            return redirect('listar_facturaciones')
        facturacion.estado = 'Anulado'
        facturacion.save()
        return redirect('listar_facturaciones')
    # Si no es POST, mostrar confirmación
    return render(request, 'anular_facturacion.html', {'facturacion': facturacion})
