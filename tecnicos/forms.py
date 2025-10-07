from django import forms
from django.contrib.auth.models import User
from .models import Tecnico, VacacionesTecnico, DocumentoTecnico, Especialidad

class TecnicoForm(forms.ModelForm):
    # Campos del usuario
    first_name = forms.CharField(
        max_length=150,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Tecnico
        fields = [
            'codigo_empleado', 'rut', 'fecha_nacimiento', 'ubicacion', 'departamento', 
            'puesto', 'fecha_ingreso', 'telefono', 'direccion', 'telefono_emergencia', 
            'nombre_emergencia', 'linkedin', 'prevision', 'afp', 'salario_base', 
            'estado', 'especialidades', 'foto', 'postre_favorito', 'observaciones'
        ]
        
        widgets = {
            'codigo_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'nombre_emergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/usuario'}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'afp': forms.Select(attrs={'class': 'form-select'}),
            'salario_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'especialidades': forms.CheckboxSelectMultiple(),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'postre_favorito': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        labels = {
            'codigo_empleado': 'Código de Empleado',
            'rut': 'RUT',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'ubicacion': 'Ubicación',
            'departamento': 'Departamento',
            'puesto': 'Puesto',
            'fecha_ingreso': 'Fecha de Ingreso',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'telefono_emergencia': 'Teléfono de Emergencia',
            'nombre_emergencia': 'Contacto de Emergencia',
            'linkedin': 'LinkedIn',
            'prevision': 'Previsión',
            'afp': 'AFP',
            'salario_base': 'Salario Base',
            'estado': 'Estado',
            'especialidades': 'Especialidades',
            'foto': 'Foto de Perfil',
            'postre_favorito': 'Postre Favorito',
            'observaciones': 'Observaciones',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidades'].queryset = Especialidad.objects.filter(activa=True)
        
        # Si estamos editando, llenar los campos del usuario
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario'):
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email

class VacacionesForm(forms.ModelForm):
    class Meta:
        model = VacacionesTecnico
        fields = ['fecha_inicio', 'fecha_fin', 'dias_solicitados', 'motivo']
        
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dias_solicitados': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        labels = {
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'dias_solicitados': 'Días Solicitados',
            'motivo': 'Motivo',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
            
            # Calcular días automáticamente
            dias_calculados = (fecha_fin - fecha_inicio).days + 1
            cleaned_data['dias_solicitados'] = dias_calculados
        
        return cleaned_data

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoTecnico
        fields = ['tipo', 'nombre', 'archivo', 'descripcion']
        
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'tipo': 'Tipo de Documento',
            'nombre': 'Nombre del Documento',
            'archivo': 'Archivo',
            'descripcion': 'Descripción',
        }

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'activa']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'nombre': 'Nombre de la Especialidad',
            'descripcion': 'Descripción',
            'activa': 'Activa',
        }
