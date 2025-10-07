from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from .models import Producto, Categoria, Proveedor, MovimientoInventario
from .forms import ProductoForm, CategoriaForm, ProveedorForm, MovimientoInventarioForm

@login_required
def producto_list(request):
    # Filtros de búsqueda
    search = request.GET.get('search', '')
    categoria = request.GET.get('categoria', '')
    proveedor = request.GET.get('proveedor', '')
    bajo_stock = request.GET.get('bajo_stock', '')
    
    productos = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)
    
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) | 
            Q(codigo__icontains=search) |
            Q(descripcion__icontains=search)
        )
    
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    
    if proveedor:
        productos = productos.filter(proveedor_id=proveedor)
    
    if bajo_stock:
        productos = productos.filter(stock_actual__lte=F('stock_minimo'))
    
    productos = productos.order_by('nombre')
    
    # Para los filtros
    categorias = Categoria.objects.filter(activa=True)
    proveedores = Proveedor.objects.filter(activo=True)
    
    # Formulario vacío para el modal
    form = ProductoForm()
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'proveedores': proveedores,
        'search': search,
        'categoria_selected': categoria,
        'proveedor_selected': proveedor,
        'bajo_stock': bajo_stock,
        'form': form,
    }
    
    return render(request, 'productos/list.html', context)

@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    movimientos = producto.movimientos.all()[:10]
    
    context = {
        'producto': producto,
        'movimientos': movimientos,
    }
    return render(request, 'productos/detail.html', context)

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            
            # Crear movimiento inicial si hay stock
            if producto.stock_actual > 0:
                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='entrada',
                    cantidad=producto.stock_actual,
                    stock_anterior=0,
                    stock_nuevo=producto.stock_actual,
                    motivo='Stock inicial',
                    usuario=request.user
                )
            
            messages.success(request, f'Producto {producto.nombre} creado exitosamente.')
            return redirect('productos:detail', pk=producto.pk)
    else:
        form = ProductoForm()
    
    return render(request, 'productos/form.html', {
        'form': form,
        'title': 'Nuevo Producto',
        'action': 'Crear'
    })

@login_required
def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    stock_anterior = producto.stock_actual
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            
            # Si cambió el stock, crear movimiento
            if producto.stock_actual != stock_anterior:
                diferencia = producto.stock_actual - stock_anterior
                tipo = 'entrada' if diferencia > 0 else 'salida'
                
                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='ajuste',
                    cantidad=diferencia,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock_actual,
                    motivo='Ajuste manual',
                    usuario=request.user
                )
            
            messages.success(request, f'Producto {producto.nombre} actualizado exitosamente.')
            return redirect('productos:detail', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/form.html', {
        'form': form,
        'producto': producto,
        'title': f'Editar Producto - {producto.nombre}',
        'action': 'Actualizar'
    })

@login_required
def movimiento_create(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.producto = producto
            movimiento.usuario = request.user
            movimiento.stock_anterior = producto.stock_actual
            
            # Calcular nuevo stock
            if movimiento.tipo == 'entrada':
                nuevo_stock = producto.stock_actual + movimiento.cantidad
            elif movimiento.tipo == 'salida':
                nuevo_stock = max(0, producto.stock_actual - movimiento.cantidad)
            else:  # ajuste
                nuevo_stock = movimiento.cantidad
            
            movimiento.stock_nuevo = nuevo_stock
            movimiento.save()
            
            # Actualizar stock del producto
            producto.stock_actual = nuevo_stock
            producto.save()
            
            messages.success(request, 'Movimiento de inventario registrado exitosamente.')
            return redirect('productos:detail', pk=producto.pk)
    else:
        form = MovimientoInventarioForm()
    
    return render(request, 'productos/movimiento_form.html', {
        'form': form,
        'producto': producto,
        'title': f'Nuevo Movimiento - {producto.nombre}'
    })

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'Producto {producto.nombre} eliminado exitosamente.')
        return redirect('productos:list')

    context = {
        'producto': producto,
        'title': f'Eliminar Producto - {producto.nombre}'
    }

    return render(request, 'productos/delete_confirm.html', context)
