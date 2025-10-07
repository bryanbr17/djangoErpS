from django.db import models
from django.contrib.auth.models import User

class ConfiguracionSistema(models.Model):
    """Configuraciones generales del sistema"""
    
    # Información de la empresa
    nombre_empresa = models.CharField(max_length=200, default='Mi Empresa')
    rut_empresa = models.CharField(max_length=20, blank=True)
    direccion_empresa = models.TextField(blank=True)
    telefono_empresa = models.CharField(max_length=20, blank=True)
    email_empresa = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    
    # Configuración de facturación
    moneda_principal = models.CharField(max_length=10, default='CLP')
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    formato_factura = models.CharField(max_length=50, default='FAC-{numero}')
    
    # Configuración de sistema
    zona_horaria = models.CharField(max_length=50, default='America/Santiago')
    idioma = models.CharField(max_length=10, default='es')
    formato_fecha = models.CharField(max_length=20, default='%d/%m/%Y')
    
    # Configuración de notificaciones
    email_notificaciones = models.BooleanField(default=True)
    smtp_servidor = models.CharField(max_length=100, blank=True)
    smtp_puerto = models.IntegerField(default=587)
    smtp_usuario = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_tls = models.BooleanField(default=True)
    
    # Configuración de respaldos
    respaldo_automatico = models.BooleanField(default=False)
    frecuencia_respaldo = models.CharField(max_length=20, default='semanal')
    ruta_respaldos = models.CharField(max_length=500, blank=True)
    
    # Configuración de seguridad
    sesion_timeout = models.IntegerField(default=30)  # minutos
    intentos_login_max = models.IntegerField(default=5)
    bloqueo_tiempo = models.IntegerField(default=15)  # minutos
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
    
    def __str__(self):
        return f"Configuración - {self.nombre_empresa}"
    
    @classmethod
    def get_config(cls):
        """Obtiene la configuración actual o crea una por defecto"""
        config, created = cls.objects.get_or_create(pk=1)
        return config

class ConfiguracionModulo(models.Model):
    """Configuraciones específicas por módulo"""
    
    MODULOS_CHOICES = [
        ('tecnicos', 'Técnicos'),
        ('productos', 'Productos'),
        ('cotizaciones', 'Cotizaciones'),
        ('reportes', 'Reportes'),
        ('dashboard', 'Dashboard'),
    ]
    
    modulo = models.CharField(max_length=50, choices=MODULOS_CHOICES)
    clave = models.CharField(max_length=100)
    valor = models.TextField()
    descripcion = models.TextField(blank=True)
    tipo_dato = models.CharField(max_length=20, default='string')  # string, integer, boolean, json
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Configuración de Módulo"
        verbose_name_plural = "Configuraciones de Módulos"
        unique_together = ['modulo', 'clave']
    
    def __str__(self):
        return f"{self.modulo} - {self.clave}"
    
    def get_valor_typed(self):
        """Retorna el valor convertido al tipo correcto"""
        if self.tipo_dato == 'integer':
            return int(self.valor)
        elif self.tipo_dato == 'boolean':
            return self.valor.lower() in ['true', '1', 'yes']
        elif self.tipo_dato == 'json':
            import json
            return json.loads(self.valor)
        return self.valor

class LogConfiguracion(models.Model):
    """Log de cambios en configuraciones"""
    
    modulo = models.CharField(max_length=50)
    clave = models.CharField(max_length=100)
    valor_anterior = models.TextField(blank=True)
    valor_nuevo = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Log de Configuración"
        verbose_name_plural = "Logs de Configuración"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.modulo}.{self.clave} - {self.fecha}"
