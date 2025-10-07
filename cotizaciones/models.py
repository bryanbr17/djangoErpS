from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from productos.models import Producto
from tecnicos.models import Tecnico


class Cliente(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('persona', 'Persona Natural'),
        ('empresa', 'Empresa'),
    ]

    # Información básica
    tipo = models.CharField(
        max_length=20, choices=TIPO_CLIENTE_CHOICES, default='persona')
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    # Información adicional
    contacto_principal = models.CharField(
        max_length=100, blank=True)  # Para empresas
    giro = models.CharField(max_length=200, blank=True)  # Para empresas

    # Estado
    activo = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.rut} - {self.nombre}"


class Cotizacion(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('vencida', 'Vencida'),
        ('facturada', 'Facturada'),
    ]

    # Información básica
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='cotizaciones')
    tecnico_asignado = models.ForeignKey(
        Tecnico, on_delete=models.SET_NULL, null=True, blank=True)

    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateField()
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    # Información comercial
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)  # Porcentaje
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Estado y observaciones
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='borrador')
    observaciones = models.TextField(blank=True)
    condiciones_comerciales = models.TextField(blank=True)

    # Usuario que creó la cotización
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"COT-{self.numero} - {self.cliente.nombre}"

    def get_absolute_url(self):
        return reverse('cotizaciones:detail', kwargs={'pk': self.pk})

    def calcular_totales(self):
        """Calcula los totales de la cotización basado en los items"""
        items = self.items.all()
        self.subtotal = sum(item.total for item in items)
        descuento_monto = self.subtotal * (self.descuento / 100)
        subtotal_con_descuento = self.subtotal - descuento_monto
        self.impuestos = subtotal_con_descuento * 0.19  # IVA 19%
        self.total = subtotal_con_descuento + self.impuestos
        self.save()


class ItemCotizacion(models.Model):
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    # Información del item
    descripcion = models.TextField(blank=True)  # Descripción personalizada
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_item = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)  # Porcentaje
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Orden de los items
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Item de Cotización"
        verbose_name_plural = "Items de Cotización"
        ordering = ['orden']

    def save(self, *args, **kwargs):
        # Calcular total automáticamente
        subtotal = self.cantidad * self.precio_unitario
        descuento_monto = subtotal * (self.descuento_item / 100)
        self.total = subtotal - descuento_monto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cotizacion.numero} - {self.producto.nombre}"


class SeguimientoCotizacion(models.Model):
    TIPO_SEGUIMIENTO_CHOICES = [
        ('creacion', 'Creación'),
        ('envio', 'Envío'),
        ('respuesta_cliente', 'Respuesta del Cliente'),
        ('modificacion', 'Modificación'),
        ('aprobacion', 'Aprobación'),
        ('rechazo', 'Rechazo'),
        ('vencimiento', 'Vencimiento'),
        ('facturacion', 'Facturación'),
        ('nota', 'Nota'),
    ]

    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE, related_name='seguimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_SEGUIMIENTO_CHOICES)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Seguimiento de Cotización"
        verbose_name_plural = "Seguimientos de Cotización"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.cotizacion.numero} - {self.tipo} - {self.fecha.strftime('%d/%m/%Y')}"
