from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from tecnicos.models import Tecnico, VacacionesTecnico
from productos.models import Producto, MovimientoInventario
from cotizaciones.models import Cotizacion, Cliente

@login_required
def dashboard_index(request):
    """Vista principal del dashboard con métricas generales"""
    
    # Métricas de técnicos
    total_tecnicos = Tecnico.objects.count()
    tecnicos_activos = Tecnico.objects.filter(estado='activo').count()
    tecnicos_vacaciones = Tecnico.objects.filter(estado='vacaciones').count()
    
    # Métricas de productos
    total_productos = Producto.objects.filter(activo=True).count()
    productos_bajo_stock = Producto.objects.filter(
        activo=True,
        stock_actual__lte=F('stock_minimo')
    ).count()
    
    # Métricas de cotizaciones (último mes)
    fecha_inicio_mes = timezone.now().replace(day=1)
    cotizaciones_mes = Cotizacion.objects.filter(
        fecha_creacion__gte=fecha_inicio_mes
    )
    
    total_cotizaciones_mes = cotizaciones_mes.count()
    cotizaciones_aprobadas = cotizaciones_mes.filter(estado='aprobada').count()
    valor_cotizaciones_mes = cotizaciones_mes.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Métricas de clientes
    total_clientes = Cliente.objects.filter(activo=True).count()
    
    # Cotizaciones recientes
    cotizaciones_recientes = Cotizacion.objects.select_related(
        'cliente', 'tecnico_asignado'
    ).order_by('-fecha_creacion')[:5]
    
    # Productos con bajo stock
    productos_restock = Producto.objects.filter(
        activo=True,
        stock_actual__lte=F('stock_minimo')
    ).order_by('stock_actual')[:5]
    
    # Vacaciones pendientes
    vacaciones_pendientes = VacacionesTecnico.objects.filter(
        estado='pendiente'
    ).select_related('tecnico').order_by('fecha_inicio')[:5]
    
    # Agregar datos para gráficos al contexto
    context = {
        'total_tecnicos': total_tecnicos,
        'tecnicos_activos': tecnicos_activos,
        'tecnicos_vacaciones': tecnicos_vacaciones,
        'total_productos': total_productos,
        'productos_bajo_stock': productos_bajo_stock,
        'total_cotizaciones_mes': total_cotizaciones_mes,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'valor_cotizaciones_mes': valor_cotizaciones_mes,
        'total_clientes': total_clientes,
        'cotizaciones_recientes': cotizaciones_recientes,
        'productos_restock': productos_restock,
        'vacaciones_pendientes': vacaciones_pendientes,
        # Datos para gráficos
        'grafico_cotizaciones_labels': ['Borradores', 'Enviadas', 'Aprobadas', 'Rechazadas'],
        'grafico_cotizaciones_data': [15, 8, 12, 3],
        'grafico_ventas_labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'grafico_ventas_data': [12000, 19000, 15000, 25000, 22000, 30000],
    }
    
    return render(request, 'dashboard/index.html', context)
