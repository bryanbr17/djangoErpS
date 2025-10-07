#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from django.contrib.auth.models import User
from tecnicos.models import Tecnico
from datetime import date

def crear_tecnicos_prueba():
    print("=== Verificando técnicos existentes ===")
    tecnicos_existentes = Tecnico.objects.all()
    print(f"Técnicos encontrados: {tecnicos_existentes.count()}")
    
    for tecnico in tecnicos_existentes:
        print(f"- {tecnico.usuario.first_name} {tecnico.usuario.last_name} ({tecnico.usuario.username})")
    
    if tecnicos_existentes.count() == 0:
        print("\n=== Creando técnicos de prueba ===")
        
        # Crear usuarios y técnicos de prueba
        tecnicos_data = [
            {
                'username': 'carlos_lopez',
                'first_name': 'Carlos',
                'last_name': 'López',
                'email': 'carlos.lopez@setel.com',
                'telefono': '+56912345678',
                'direccion': 'Av. Providencia 1234, Santiago'
            },
            {
                'username': 'maria_gonzalez',
                'first_name': 'María',
                'last_name': 'González',
                'email': 'maria.gonzalez@setel.com',
                'telefono': '+56987654321',
                'direccion': 'Calle Los Leones 567, Las Condes'
            },
            {
                'username': 'juan_martinez',
                'first_name': 'Juan',
                'last_name': 'Martínez',
                'email': 'juan.martinez@setel.com',
                'telefono': '+56955555555',
                'direccion': 'Av. Libertador 890, Ñuñoa'
            }
        ]
        
        for data in tecnicos_data:
            # Crear usuario
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('123456')  # Contraseña temporal
                user.save()
                print(f"Usuario creado: {user.username}")
            
            # Crear técnico
            tecnico, created = Tecnico.objects.get_or_create(
                usuario=user,
                defaults={
                    'telefono': data['telefono'],
                    'direccion': data['direccion'],
                    'fecha_ingreso': date.today(),
                    'estado': 'activo'
                }
            )
            
            if created:
                print(f"Técnico creado: {tecnico.usuario.get_full_name()}")
            else:
                print(f"Técnico ya existe: {tecnico.usuario.get_full_name()}")
    
    print("\n=== Resumen final ===")
    total_tecnicos = Tecnico.objects.all().count()
    print(f"Total de técnicos en la base de datos: {total_tecnicos}")
    
    print("\n=== Lista de técnicos ===")
    for tecnico in Tecnico.objects.all():
        print(f"ID: {tecnico.id} - {tecnico.usuario.get_full_name()} ({tecnico.usuario.username})")
        print(f"   Email: {tecnico.usuario.email}")
        print(f"   Teléfono: {tecnico.telefono}")
        print(f"   Estado: {tecnico.get_estado_display()}")
        print("---")

if __name__ == '__main__':
    crear_tecnicos_prueba()
