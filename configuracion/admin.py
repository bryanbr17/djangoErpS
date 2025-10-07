from django.contrib import admin
from .models import ConfiguracionSistema, ConfiguracionModulo, LogConfiguracion

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'moneda_principal', 'updated_at', 'updated_by']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('nombre_empresa', 'rut_empresa', 'direccion_empresa', 'telefono_empresa', 'email_empresa', 'sitio_web')
        }),
        ('Configuración Comercial', {
            'fields': ('moneda_principal', 'iva_porcentaje', 'formato_factura')
        }),
        ('Configuración Regional', {
            'fields': ('zona_horaria', 'idioma', 'formato_fecha')
        }),
        ('Notificaciones', {
            'fields': ('email_notificaciones', 'smtp_servidor', 'smtp_puerto', 'smtp_usuario', 'smtp_password', 'smtp_tls')
        }),
        ('Respaldos', {
            'fields': ('respaldo_automatico', 'frecuencia_respaldo', 'ruta_respaldos')
        }),
        ('Seguridad', {
            'fields': ('sesion_timeout', 'intentos_login_max', 'bloqueo_tiempo')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'updated_by')
        }),
    )

@admin.register(ConfiguracionModulo)
class ConfiguracionModuloAdmin(admin.ModelAdmin):
    list_display = ['modulo', 'clave', 'tipo_dato', 'updated_at', 'updated_by']
    list_filter = ['modulo', 'tipo_dato']
    search_fields = ['clave', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LogConfiguracion)
class LogConfiguracionAdmin(admin.ModelAdmin):
    list_display = ['modulo', 'clave', 'usuario', 'fecha', 'ip_address']
    list_filter = ['modulo', 'fecha', 'usuario']
    search_fields = ['clave', 'valor_nuevo']
    readonly_fields = ['fecha']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
