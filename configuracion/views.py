from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import ConfiguracionSistema, ConfiguracionModulo, LogConfiguracion

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def configuracion_index(request):
    """Vista principal de configuración con todas las opciones"""
    
    # Opciones de configuración organizadas por categorías
    configuration_options = [
        {
            'category': 'Sistema',
            'options': [
                {'id': 'general', 'title': 'General', 'icon': 'bi-gear', 'description': 'Configuración general del sistema'},
                {'id': 'usuarios', 'title': 'Gestión de Usuarios', 'icon': 'bi-people', 'description': 'Administrar usuarios y permisos'},
                {'id': 'seguridad', 'title': 'Seguridad', 'icon': 'bi-shield-check', 'description': 'Configurar políticas de seguridad'},
                {'id': 'auditoria', 'title': 'Auditoría', 'icon': 'bi-clock-history', 'description': 'Configurar logs y auditoría'},
            ]
        },
        {
            'category': 'Comunicaciones',
            'options': [
                {'id': 'correo', 'title': 'Servidor de Correo', 'icon': 'bi-envelope', 'description': 'Configurar servidor SMTP'},
                {'id': 'notificaciones', 'title': 'Notificaciones', 'icon': 'bi-bell', 'description': 'Configurar alertas y notificaciones'},
            ]
        },
        {
            'category': 'Comercial',
            'options': [
                {'id': 'facturacion', 'title': 'Facturación', 'icon': 'bi-file-text', 'description': 'Configurar facturación y documentos'},
                {'id': 'pagos', 'title': 'Pasarelas de Pago', 'icon': 'bi-credit-card', 'description': 'Configurar métodos de pago'},
                {'id': 'moneda', 'title': 'Moneda y Precios', 'icon': 'bi-currency-dollar', 'description': 'Configurar monedas y precios'},
            ]
        },
        {
            'category': 'Datos',
            'options': [
                {'id': 'base-datos', 'title': 'Base de Datos', 'icon': 'bi-database', 'description': 'Configuración de base de datos'},
                {'id': 'respaldos', 'title': 'Respaldos', 'icon': 'bi-hdd', 'description': 'Configurar copias de seguridad'},
                {'id': 'importar', 'title': 'Importar Datos', 'icon': 'bi-upload', 'description': 'Importar datos desde archivos'},
                {'id': 'exportar', 'title': 'Exportar Datos', 'icon': 'bi-download', 'description': 'Exportar datos del sistema'},
            ]
        },
        {
            'category': 'Personalización',
            'options': [
                {'id': 'tema', 'title': 'Personalización', 'icon': 'bi-palette', 'description': 'Personalizar apariencia del sistema'},
                {'id': 'plantillas', 'title': 'Editor de Plantillas', 'icon': 'bi-code-slash', 'description': 'Personalizar plantillas del sistema'},
                {'id': 'reportes', 'title': 'Reportes', 'icon': 'bi-bar-chart', 'description': 'Configurar reportes automáticos'},
            ]
        },
        {
            'category': 'Integraciones',
            'options': [
                {'id': 'api', 'title': 'API y Webhooks', 'icon': 'bi-globe', 'description': 'Configurar integraciones externas'},
                {'id': 'cloud', 'title': 'Servicios Cloud', 'icon': 'bi-cloud', 'description': 'Configurar servicios en la nube'},
            ]
        }
    ]
    
    return render(request, 'configuracion/index.html', {
        'configuration_options': configuration_options
    })

@login_required
@user_passes_test(is_admin)
def configuracion_general(request):
    """Configuración general del sistema"""
    config = ConfiguracionSistema.get_config()
    
    if request.method == 'POST':
        # Actualizar configuración
        config.nombre_empresa = request.POST.get('nombre_empresa', config.nombre_empresa)
        config.rut_empresa = request.POST.get('rut_empresa', config.rut_empresa)
        config.direccion_empresa = request.POST.get('direccion_empresa', config.direccion_empresa)
        config.telefono_empresa = request.POST.get('telefono_empresa', config.telefono_empresa)
        config.email_empresa = request.POST.get('email_empresa', config.email_empresa)
        config.sitio_web = request.POST.get('sitio_web', config.sitio_web)
        config.moneda_principal = request.POST.get('moneda_principal', config.moneda_principal)
        config.iva_porcentaje = request.POST.get('iva_porcentaje', config.iva_porcentaje)
        config.zona_horaria = request.POST.get('zona_horaria', config.zona_horaria)
        config.idioma = request.POST.get('idioma', config.idioma)
        config.updated_by = request.user
        
        config.save()
        
        # Registrar en log
        LogConfiguracion.objects.create(
            modulo='sistema',
            clave='configuracion_general',
            valor_nuevo='Configuración general actualizada',
            usuario=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Configuración general actualizada correctamente.')
        return redirect('configuracion:general')
    
    return render(request, 'configuracion/general.html', {'config': config})

@login_required
@user_passes_test(is_admin)
def configuracion_correo(request):
    """Configuración del servidor de correo"""
    config = ConfiguracionSistema.get_config()
    
    if request.method == 'POST':
        config.email_notificaciones = 'email_notificaciones' in request.POST
        config.smtp_servidor = request.POST.get('smtp_servidor', config.smtp_servidor)
        config.smtp_puerto = int(request.POST.get('smtp_puerto', config.smtp_puerto))
        config.smtp_usuario = request.POST.get('smtp_usuario', config.smtp_usuario)
        if request.POST.get('smtp_password'):
            config.smtp_password = request.POST.get('smtp_password')
        config.smtp_tls = 'smtp_tls' in request.POST
        config.updated_by = request.user
        
        config.save()
        
        LogConfiguracion.objects.create(
            modulo='sistema',
            clave='configuracion_correo',
            valor_nuevo='Configuración de correo actualizada',
            usuario=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Configuración de correo actualizada correctamente.')
        return redirect('configuracion:correo')
    
    return render(request, 'configuracion/correo.html', {'config': config})

@login_required
@user_passes_test(is_admin)
def configuracion_seguridad(request):
    """Configuración de seguridad"""
    config = ConfiguracionSistema.get_config()
    
    if request.method == 'POST':
        config.sesion_timeout = int(request.POST.get('sesion_timeout', config.sesion_timeout))
        config.intentos_login_max = int(request.POST.get('intentos_login_max', config.intentos_login_max))
        config.bloqueo_tiempo = int(request.POST.get('bloqueo_tiempo', config.bloqueo_tiempo))
        config.updated_by = request.user
        
        config.save()
        
        LogConfiguracion.objects.create(
            modulo='sistema',
            clave='configuracion_seguridad',
            valor_nuevo='Configuración de seguridad actualizada',
            usuario=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Configuración de seguridad actualizada correctamente.')
        return redirect('configuracion:seguridad')
    
    return render(request, 'configuracion/seguridad.html', {'config': config})

@login_required
@user_passes_test(is_admin)
def configuracion_respaldos(request):
    """Configuración de respaldos"""
    config = ConfiguracionSistema.get_config()
    
    if request.method == 'POST':
        config.respaldo_automatico = 'respaldo_automatico' in request.POST
        config.frecuencia_respaldo = request.POST.get('frecuencia_respaldo', config.frecuencia_respaldo)
        config.ruta_respaldos = request.POST.get('ruta_respaldos', config.ruta_respaldos)
        config.updated_by = request.user
        
        config.save()
        
        LogConfiguracion.objects.create(
            modulo='sistema',
            clave='configuracion_respaldos',
            valor_nuevo='Configuración de respaldos actualizada',
            usuario=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Configuración de respaldos actualizada correctamente.')
        return redirect('configuracion:respaldos')
    
    return render(request, 'configuracion/respaldos.html', {'config': config})
