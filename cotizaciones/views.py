from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from django.db import transaction
from .models import Cotizacion, Cliente, ItemCotizacion

def generar_numero_cotizacion():
    """Genera un número único para la cotización"""
    import random
    
    # Obtener el año actual
    year = date.today().year
    
    # Intentar generar un número único
    for _ in range(100):  # Máximo 100 intentos
        # Generar número aleatorio de 4 dígitos
        numero_aleatorio = random.randint(1000, 9999)
        numero = f"{year}{numero_aleatorio}"
        
        # Verificar si ya existe
        if not Cotizacion.objects.filter(numero=numero).exists():
            return numero
    
    # Si no se pudo generar después de 100 intentos, usar timestamp
    import time
    timestamp = int(time.time())
    return f"{year}{timestamp % 10000}"

@login_required
def cotizacion_list(request):
    # Filtros de búsqueda
    folio = request.GET.get('folio', '')
    rut = request.GET.get('rut', '')
    razon_social = request.GET.get('razon_social', '')
    contacto = request.GET.get('contacto', '')
    detalle = request.GET.get('detalle', '')
    año = request.GET.get('año', 'todos')
    fecha_emision = request.GET.get('fecha_emision', '')
    estado = request.GET.get('estado', 'todas')
    tipo = request.GET.get('tipo', 'todas')
    vendedor = request.GET.get('vendedor', 'todos')
    
    cotizaciones = Cotizacion.objects.select_related('cliente').all()
    
    # Debug: mostrar total de cotizaciones
    print(f"=== DEBUG LISTA COTIZACIONES ===")
    print(f"Total cotizaciones en BD: {Cotizacion.objects.count()}")
    print(f"Estado filtro: {estado}")
    
    # Aplicar filtros
    if folio:
        cotizaciones = cotizaciones.filter(numero__icontains=folio)
    
    if rut:
        cotizaciones = cotizaciones.filter(cliente__rut__icontains=rut)
    
    if razon_social:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=razon_social)
    
    if contacto:
        cotizaciones = cotizaciones.filter(cliente__contacto_principal__icontains=contacto)
    
    if detalle:
        cotizaciones = cotizaciones.filter(observaciones__icontains=detalle)
    
    if año != 'todos':
        cotizaciones = cotizaciones.filter(fecha_creacion__year=año)
    
    if fecha_emision:
        cotizaciones = cotizaciones.filter(fecha_creacion=fecha_emision)
    
    # Filtros de estado corregidos
    if estado == 'borrador':
        cotizaciones = cotizaciones.filter(estado='borrador')
    elif estado == 'enviada':
        cotizaciones = cotizaciones.filter(estado='enviada')
    elif estado == 'aprobada':
        cotizaciones = cotizaciones.filter(estado='aprobada')
    elif estado == 'rechazada':
        cotizaciones = cotizaciones.filter(estado='rechazada')
    # Si es 'todas', no aplicar filtro de estado
    
    if tipo == 'afecta':
        cotizaciones = cotizaciones.filter(tipo='afecta')
    elif tipo == 'exenta':
        cotizaciones = cotizaciones.filter(tipo='exenta')
    
    if vendedor != 'todos':
        cotizaciones = cotizaciones.filter(creado_por__username=vendedor)
    
    cotizaciones = cotizaciones.order_by('-fecha_creacion')
    
    # Debug final
    print(f"Cotizaciones después de filtros: {cotizaciones.count()}")
    for cot in cotizaciones[:3]:  # Mostrar las primeras 3
        print(f"  - {cot.numero} | {cot.cliente.nombre if cot.cliente else 'Sin cliente'} | {cot.estado}")
    
    # Opciones para los filtros
    años_disponibles = Cotizacion.objects.dates('fecha_creacion', 'year', order='DESC')
    vendedores = Cotizacion.objects.values_list('creado_por__username', flat=True).distinct()
    
    context = {
        'cotizaciones': cotizaciones,
        'folio': folio,
        'rut': rut,
        'razon_social': razon_social,
        'contacto': contacto,
        'detalle': detalle,
        'año': año,
        'fecha_emision': fecha_emision,
        'estado': estado,
        'tipo': tipo,
        'vendedor': vendedor,
        'años_disponibles': años_disponibles,
        'vendedores': vendedores,
    }
    
    return render(request, 'cotizaciones/list.html', context)

@login_required
def cotizacion_detail(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    items = cotizacion.items.all()
    
    context = {
        'cotizacion': cotizacion,
        'items': items,
    }
    return render(request, 'cotizaciones/detail.html', context)

@login_required
def cotizacion_create(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Debug: imprimir datos recibidos
                print("=== DEBUG COTIZACIÓN ===")
                print(f"POST data: {dict(request.POST)}")
                
                # Procesar el formulario
                rut_cliente = request.POST.get('rut_cliente', '').strip()
                razon_social = request.POST.get('razon_social', '').strip()
                folio_manual = request.POST.get('folio', '').strip()
                moneda = request.POST.get('moneda', 'CLP')
                vendedor = request.POST.get('vendedor', '')
                glosa_adicional = request.POST.get('glosa_adicional', '')
                
                print(f"RUT Cliente: '{rut_cliente}'")
                print(f"Razón Social: '{razon_social}'")
                print(f"Folio: '{folio_manual}'")
                
                # Validar campos requeridos
                if not rut_cliente:
                    messages.error(request, 'El RUT del cliente es requerido.')
                    return render(request, 'cotizaciones/emitir.html', {'numero_sugerido': generar_numero_cotizacion()})
                
                if not razon_social:
                    messages.error(request, 'La razón social del cliente es requerida.')
                    return render(request, 'cotizaciones/emitir.html', {'numero_sugerido': generar_numero_cotizacion()})
                
                # Generar número de cotización único
                if folio_manual and not Cotizacion.objects.filter(numero=folio_manual).exists():
                    numero_cotizacion = folio_manual
                else:
                    numero_cotizacion = generar_numero_cotizacion()
                    if folio_manual:
                        messages.warning(request, f'El folio {folio_manual} ya existe. Se generó automáticamente: {numero_cotizacion}')
                
                # Crear cliente si no existe
                cliente, created = Cliente.objects.get_or_create(
                    rut=rut_cliente,
                    defaults={
                        'nombre': razon_social,
                        'contacto_principal': request.POST.get('nombre_contacto', ''),
                        'email': request.POST.get('email_contacto', ''),
                        'telefono': request.POST.get('fono_contacto', ''),
                        'tipo': 'empresa'
                    }
                )
                
                # Crear cotización
                fecha_vencimiento = date.today() + timedelta(days=30)  # 30 días por defecto
                
                cotizacion = Cotizacion.objects.create(
                    cliente=cliente,
                    numero=numero_cotizacion,
                    fecha_vencimiento=fecha_vencimiento,
                    observaciones=glosa_adicional,
                    creado_por=request.user,
                    estado='borrador'
                )
                
                print(f"✅ Cotización creada: ID={cotizacion.id}, Número={cotizacion.numero}")
                messages.success(request, f'¡Cotización {cotizacion.numero} creada exitosamente! Cliente: {cliente.nombre}')
                return redirect('cotizaciones:detail', pk=cotizacion.pk)
                
        except Exception as e:
            messages.error(request, f'Error al crear la cotización: {str(e)}')
            return render(request, 'cotizaciones/emitir.html')
    
    # GET request - mostrar formulario con número sugerido
    numero_sugerido = generar_numero_cotizacion()
    context = {
        'numero_sugerido': numero_sugerido
    }
    return render(request, 'cotizaciones/emitir.html', context)

@login_required
def cotizacion_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    messages.info(request, f'Formulario de edición para {cotizacion.folio} en desarrollo.')
    return redirect('cotizaciones:detail', pk=cotizacion.pk)

@login_required
def cotizacion_aprobar(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    cotizacion.estado = 'aprobada'
    cotizacion.save()
    
    messages.success(request, f'Cotización {cotizacion.numero} aprobada exitosamente.')
    return redirect('cotizaciones:detail', pk=cotizacion.pk)

@login_required
def cotizacion_rechazar(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    cotizacion.estado = 'rechazada'
    cotizacion.save()
    
    messages.success(request, f'Cotización {cotizacion.numero} rechazada.')
    return redirect('cotizaciones:detail', pk=cotizacion.pk)

@login_required
def cotizacion_delete(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    if request.method == 'POST':
        cotizacion.delete()
        messages.success(request, f'Cotización {cotizacion.numero} eliminada exitosamente.')
        return redirect('cotizaciones:list')

    context = {
        'cotizacion': cotizacion,
        'title': f'Eliminar Cotización - {cotizacion.numero}'
    }

    return render(request, 'cotizaciones/delete_confirm.html', context)
