#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from cotizaciones.models import Cotizacion, Cliente

def test_lista_cotizaciones():
    print("=== TEST LISTA COTIZACIONES ===")
    
    # Obtener todas las cotizaciones
    cotizaciones = Cotizacion.objects.select_related('cliente').all()
    
    print(f"Total cotizaciones: {cotizaciones.count()}")
    
    if cotizaciones.count() == 0:
        print("❌ No hay cotizaciones en la base de datos")
        return
    
    print("\n=== COTIZACIONES ENCONTRADAS ===")
    for cot in cotizaciones:
        cliente_nombre = cot.cliente.nombre if cot.cliente else "Sin cliente"
        print(f"ID: {cot.id}")
        print(f"  Número: {cot.numero}")
        print(f"  Cliente: {cliente_nombre}")
        print(f"  Estado: {cot.estado}")
        print(f"  Fecha: {cot.fecha_creacion}")
        print(f"  Usuario: {cot.creado_por.username if cot.creado_por else 'Sin usuario'}")
        print("---")
    
    # Probar filtros
    print("\n=== PRUEBA DE FILTROS ===")
    
    # Filtro por estado 'borrador'
    borradores = cotizaciones.filter(estado='borrador')
    print(f"Cotizaciones en borrador: {borradores.count()}")
    
    # Filtro sin estado (todas)
    todas = cotizaciones.all()
    print(f"Todas las cotizaciones: {todas.count()}")

if __name__ == '__main__':
    test_lista_cotizaciones()
