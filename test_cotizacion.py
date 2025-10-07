#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from django.contrib.auth.models import User
from cotizaciones.models import Cliente, Cotizacion
from datetime import date, timedelta

def test_crear_cotizacion():
    print("=== TEST CREAR COTIZACIÓN ===")
    
    # Obtener usuario admin
    try:
        user = User.objects.get(username='admin')
        print(f"Usuario encontrado: {user.username}")
    except User.DoesNotExist:
        user = User.objects.first()
        print(f"Usando primer usuario: {user.username if user else 'No hay usuarios'}")
    
    if not user:
        print("ERROR: No hay usuarios en el sistema")
        return
    
    # Crear cliente de prueba
    cliente, created = Cliente.objects.get_or_create(
        rut='12345678-9',
        defaults={
            'nombre': 'Empresa Test S.A.',
            'contacto_principal': 'Juan Pérez',
            'email': 'test@empresa.com',
            'telefono': '+56912345678',
            'tipo': 'empresa'
        }
    )
    
    if created:
        print(f"Cliente creado: {cliente.nombre}")
    else:
        print(f"Cliente existente: {cliente.nombre}")
    
    # Crear cotización de prueba
    try:
        cotizacion = Cotizacion.objects.create(
            cliente=cliente,
            numero='TEST2025001',
            fecha_vencimiento=date.today() + timedelta(days=30),
            observaciones='Cotización de prueba desde script',
            creado_por=user,
            estado='borrador'
        )
        
        print(f"✅ Cotización creada exitosamente:")
        print(f"   ID: {cotizacion.id}")
        print(f"   Número: {cotizacion.numero}")
        print(f"   Cliente: {cotizacion.cliente.nombre}")
        print(f"   Estado: {cotizacion.get_estado_display()}")
        print(f"   Fecha creación: {cotizacion.fecha_creacion}")
        
    except Exception as e:
        print(f"❌ Error al crear cotización: {e}")
    
    # Listar todas las cotizaciones
    print("\n=== COTIZACIONES EXISTENTES ===")
    cotizaciones = Cotizacion.objects.all().order_by('-fecha_creacion')
    for cot in cotizaciones:
        print(f"ID: {cot.id} - {cot.numero} - {cot.cliente.nombre} - {cot.get_estado_display()}")

if __name__ == '__main__':
    test_crear_cotizacion()
