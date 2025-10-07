from django.contrib import admin
from .models import Categoria, Proveedor, Producto, MovimientoInventario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'telefono', 'email', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'rut', 'email']

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 0
    readonly_fields = ['fecha']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'precio_venta', 'stock_actual', 'necesita_restock', 'activo']
    list_filter = ['categoria', 'tipo', 'activo', 'proveedor']
    search_fields = ['codigo', 'nombre', 'codigo_proveedor']
    inlines = [MovimientoInventarioInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'tipo', 'categoria')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'precio_venta', 'margen_ganancia')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo', 'stock_maximo')
        }),
        ('Proveedor', {
            'fields': ('proveedor', 'codigo_proveedor')
        }),
        ('Adicional', {
            'fields': ('imagen', 'activo')
        }),
    )
    
    def necesita_restock(self, obj):
        return obj.necesita_restock
    necesita_restock.boolean = True
    necesita_restock.short_description = 'Necesita Restock'

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo', 'cantidad', 'stock_anterior', 'stock_nuevo', 'fecha', 'usuario']
    list_filter = ['tipo', 'fecha', 'usuario']
    search_fields = ['producto__codigo', 'producto__nombre', 'motivo']
    readonly_fields = ['fecha']
