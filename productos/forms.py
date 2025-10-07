from django import forms
from .models import Producto, Categoria, Proveedor, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'descripcion', 'tipo', 'categoria',
            'precio_compra', 'precio_venta', 'margen_ganancia',
            'stock_actual', 'stock_minimo', 'stock_maximo',
            'proveedor', 'codigo_proveedor', 'imagen', 'activo'
        ]
        
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'margen_ganancia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'codigo_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'codigo': 'Código del Producto',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'tipo': 'Tipo',
            'categoria': 'Categoría',
            'precio_compra': 'Precio de Compra',
            'precio_venta': 'Precio de Venta',
            'margen_ganancia': 'Margen de Ganancia (%)',
            'stock_actual': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo',
            'stock_maximo': 'Stock Máximo',
            'proveedor': 'Proveedor',
            'codigo_proveedor': 'Código del Proveedor',
            'imagen': 'Imagen del Producto',
            'activo': 'Activo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(activa=True)
        self.fields['proveedor'].queryset = Proveedor.objects.filter(activo=True)
        self.fields['categoria'].empty_label = "Seleccionar categoría"
        self.fields['proveedor'].empty_label = "Seleccionar proveedor"
    
    def clean(self):
        cleaned_data = super().clean()
        precio_compra = cleaned_data.get('precio_compra')
        precio_venta = cleaned_data.get('precio_venta')
        stock_minimo = cleaned_data.get('stock_minimo')
        stock_maximo = cleaned_data.get('stock_maximo')
        
        if precio_compra and precio_venta:
            if precio_venta <= precio_compra:
                raise forms.ValidationError('El precio de venta debe ser mayor al precio de compra.')
        
        if stock_minimo and stock_maximo:
            if stock_minimo > stock_maximo:
                raise forms.ValidationError('El stock mínimo no puede ser mayor al stock máximo.')
        
        return cleaned_data

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activa']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
            'activa': 'Activa',
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'telefono', 'email', 'direccion', 'contacto', 'activo']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'nombre': 'Nombre del Proveedor',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'email': 'Email',
            'direccion': 'Dirección',
            'contacto': 'Persona de Contacto',
            'activo': 'Activo',
        }

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'cantidad', 'motivo', 'observaciones', 'documento_referencia']
        
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'tipo': 'Tipo de Movimiento',
            'cantidad': 'Cantidad',
            'motivo': 'Motivo',
            'observaciones': 'Observaciones',
            'documento_referencia': 'Documento de Referencia',
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad

class BusquedaProductoForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, código o descripción...'
        }),
        label='Buscar'
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoría'
    )
    
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.filter(activo=True),
        required=False,
        empty_label="Todos los proveedores",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Proveedor'
    )
    
    bajo_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Solo productos con bajo stock'
    )
