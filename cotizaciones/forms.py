from django import forms
from .models import Cotizacion, Cliente, ItemCotizacion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'razon_social', 'contacto', 'email', 'telefono', 'direccion', 'tipo']
        
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'rut': 'RUT',
            'razon_social': 'Razón Social',
            'contacto': 'Contacto',
            'email': 'Email',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'tipo': 'Tipo de Cliente',
        }

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'cliente', 'fecha_emision', 'fecha_vencimiento', 'tipo', 'moneda',
            'descuento_porcentaje', 'observaciones'
        ]
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        labels = {
            'cliente': 'Cliente',
            'fecha_emision': 'Fecha de Emisión',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'tipo': 'Tipo',
            'moneda': 'Moneda',
            'descuento_porcentaje': 'Descuento (%)',
            'observaciones': 'Observaciones',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)
        self.fields['cliente'].empty_label = "Seleccionar cliente"
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento <= fecha_emision:
                raise forms.ValidationError('La fecha de vencimiento debe ser posterior a la fecha de emisión.')
        
        return cleaned_data

class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model = ItemCotizacion
        fields = ['producto', 'descripcion', 'cantidad', 'precio_unitario', 'descuento_porcentaje']
        
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
        
        labels = {
            'producto': 'Producto',
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
            'descuento_porcentaje': 'Descuento (%)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from productos.models import Producto
        self.fields['producto'].queryset = Producto.objects.filter(activo=True)
        self.fields['producto'].empty_label = "Seleccionar producto"
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad
    
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio <= 0:
            raise forms.ValidationError('El precio unitario debe ser mayor a cero.')
        return precio

class BusquedaCotizacionForm(forms.Form):
    folio = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Folio'}),
        label='Folio'
    )
    
    rut = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
        label='RUT'
    )
    
    razon_social = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cliente'}),
        label='Razón Social'
    )
    
    contacto = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto'}),
        label='Contacto'
    )
    
    detalle = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalle'}),
        label='Detalle'
    )
    
    año = forms.ChoiceField(
        choices=[('todos', 'Todos'), ('2024', '2024'), ('2023', '2023')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Año'
    )
    
    fecha_emision = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha Emisión'
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('aprobadas_pendientes', 'Aprobadas y Pendientes'),
            ('pendiente', 'Pendiente'),
            ('aprobada', 'Aprobada'),
            ('rechazada', 'Rechazada'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado'
    )
    
    tipo = forms.ChoiceField(
        choices=[
            ('todas', 'Todas'),
            ('afecta', 'Afecta'),
            ('exenta', 'Exenta'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo'
    )
    
    vendedor = forms.ChoiceField(
        choices=[('todos', 'Todos')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Vendedor'
    )
