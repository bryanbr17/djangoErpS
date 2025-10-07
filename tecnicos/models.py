from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Tecnico(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('vacaciones', 'En Vacaciones'),
        ('licencia', 'En Licencia'),
    ]
    
    UBICACION_CHOICES = [
        ('santiago', 'Santiago'),
        ('valparaiso', 'Valparaíso'),
        ('concepcion', 'Concepción'),
        ('antofagasta', 'Antofagasta'),
        ('temuco', 'Temuco'),
        ('iquique', 'Iquique'),
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('operaciones', 'Operaciones'),
        ('mantenimiento', 'Mantenimiento'),
        ('administracion', 'Administración'),
        ('ventas', 'Ventas'),
        ('soporte', 'Soporte Técnico'),
    ]
    
    PREVISION_CHOICES = [
        ('fonasa', 'FONASA'),
        ('isapre_banmedica', 'Isapre Banmédica'),
        ('isapre_colmena', 'Isapre Colmena'),
        ('isapre_consalud', 'Isapre Consalud'),
        ('isapre_cruz_blanca', 'Isapre Cruz Blanca'),
        ('isapre_vida_tres', 'Isapre Vida Tres'),
    ]
    
    AFP_CHOICES = [
        ('afp_capital', 'AFP Capital'),
        ('afp_provida', 'AFP Provida'),
        ('afp_habitat', 'AFP Habitat'),
        ('afp_planvital', 'AFP PlanVital'),
        ('afp_cuprum', 'AFP Cuprum'),
        ('afp_modelo', 'AFP Modelo'),
    ]
    
    # Información personal
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    # Ubicación y departamento
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES, default='santiago')
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTO_CHOICES, default='operaciones')
    puesto = models.CharField(max_length=100, blank=True)
    fecha_ingreso = models.DateField()
    
    # Información de contacto
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True)
    nombre_emergencia = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    
    # Información laboral
    prevision = models.CharField(max_length=20, choices=PREVISION_CHOICES, default='fonasa')
    afp = models.CharField(max_length=20, choices=AFP_CHOICES, default='afp_capital')
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Estado y especialidades
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    especialidades = models.ManyToManyField(Especialidad, blank=True)
    
    # Información adicional
    foto = models.ImageField(upload_to='tecnicos/fotos/', null=True, blank=True)
    postre_favorito = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
        ordering = ['usuario__first_name', 'usuario__last_name']
    
    def __str__(self):
        return f"{self.codigo_empleado} - {self.usuario.get_full_name()}"
    
    def get_absolute_url(self):
        return reverse('tecnicos:detail', kwargs={'pk': self.pk})
    
    @property
    def nombre_completo(self):
        return self.usuario.get_full_name() or self.usuario.username

class DocumentoTecnico(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('cv', 'Curriculum Vitae'),
        ('certificado', 'Certificado'),
        ('contrato', 'Contrato'),
        ('identificacion', 'Identificación'),
        ('otro', 'Otro'),
    ]
    
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='tecnicos/documentos/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Documento de Técnico"
        verbose_name_plural = "Documentos de Técnicos"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.tecnico.codigo_empleado} - {self.nombre}"

class VacacionesTecnico(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('en_curso', 'En Curso'),
        ('finalizada', 'Finalizada'),
    ]
    
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='vacaciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_solicitados = models.PositiveIntegerField()
    motivo = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Aprobación
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacaciones_aprobadas')
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    comentarios_aprobacion = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Vacaciones de Técnico"
        verbose_name_plural = "Vacaciones de Técnicos"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.tecnico.codigo_empleado} - {self.fecha_inicio} a {self.fecha_fin}"
    
    @property
    def duracion_dias(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1
