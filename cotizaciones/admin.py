from django.contrib import admin
from .models import Cliente, Cotizacion, ItemCotizacion, SeguimientoCotizacion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'tipo', 'telefono', 'email', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['rut', 'nombre', 'email']

class ItemCotizacionInline(admin.TabularInline):
    model = ItemCotizacion
    extra = 0

class SeguimientoCotizacionInline(admin.TabularInline):
    model = SeguimientoCotizacion
    extra = 0
    readonly_fields = ['fecha']

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'estado', 'total', 'fecha_creacion', 'fecha_vencimiento']
    list_filter = ['estado', 'fecha_creacion', 'tecnico_asignado']
    search_fields = ['numero', 'cliente__nombre', 'cliente__rut']
    inlines = [ItemCotizacionInline, SeguimientoCotizacionInline]
    readonly_fields = ['subtotal', 'impuestos', 'total']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero', 'cliente', 'tecnico_asignado', 'creado_por')
        }),
        ('Fechas', {
            'fields': ('fecha_vencimiento', 'fecha_envio', 'fecha_respuesta')
        }),
        ('Comercial', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total')
        }),
        ('Estado y Observaciones', {
            'fields': ('estado', 'observaciones', 'condiciones_comerciales')
        }),
    )

@admin.register(ItemCotizacion)
class ItemCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'producto', 'cantidad', 'precio_unitario', 'total']
    list_filter = ['cotizacion__estado']
    search_fields = ['cotizacion__numero', 'producto__nombre']

@admin.register(SeguimientoCotizacion)
class SeguimientoCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'tipo', 'fecha', 'usuario']
    list_filter = ['tipo', 'fecha']
    search_fields = ['cotizacion__numero', 'descripcion']
    readonly_fields = ['fecha']
