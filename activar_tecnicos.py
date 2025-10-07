#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from django.contrib.auth.models import User
from tecnicos.models import Tecnico

def activar_y_corregir_tecnicos():
    print("=== Activando y corrigiendo técnicos ===")
    
    tecnicos = Tecnico.objects.all()
    
    for tecnico in tecnicos:
        print(f"\nProcesando: {tecnico.usuario.get_full_name()} (ID: {tecnico.id})")
        
        # Activar técnico
        tecnico.estado = 'activo'
        tecnico.save()
        print(f"✅ Estado cambiado a: {tecnico.get_estado_display()}")
        
        # Corregir nombres si es necesario
        user = tecnico.usuario
        
        # Corregir "bryan barra" -> "Bryan Barra"
        if user.first_name == 'bryan':
            user.first_name = 'Bryan'
            user.save()
            print(f"✅ Nombre corregido: {user.first_name}")
        
        # Corregir "barra" -> "Barra"
        if user.last_name == 'barra':
            user.last_name = 'Barra'
            user.save()
            print(f"✅ Apellido corregido: {user.last_name}")
            
        # Corregir "peralta" -> "Peralta"
        if 'peralta' in user.last_name.lower():
            user.last_name = 'Barra Peralta'
            user.save()
            print(f"✅ Apellido corregido: {user.last_name}")
            
        # Corregir "Juaquin" -> "Joaquín"
        if user.first_name == 'Juaquin':
            user.first_name = 'Joaquín'
            user.save()
            print(f"✅ Nombre corregido: {user.first_name}")
            
        # Corregir "rivas" -> "Rivas"
        if user.last_name == 'rivas':
            user.last_name = 'Rivas'
            user.save()
            print(f"✅ Apellido corregido: {user.last_name}")
    
    print("\n=== Técnicos después de las correcciones ===")
    for tecnico in Tecnico.objects.all():
        print(f"ID: {tecnico.id} - {tecnico.usuario.get_full_name()} ({tecnico.usuario.username})")
        print(f"   Estado: {tecnico.get_estado_display()}")
        print(f"   Email: {tecnico.usuario.email}")
        print("---")

if __name__ == '__main__':
    activar_y_corregir_tecnicos()
