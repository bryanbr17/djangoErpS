#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from tecnicos.forms import TecnicoForm
from django.contrib.auth.models import User

def test_formulario():
    print("=== TEST FORMULARIO TÉCNICOS ===")

    # Crear formulario vacío
    form = TecnicoForm()
    print(f"Formulario creado: {form}")

    # Verificar campos del formulario
    print("\n=== CAMPOS DEL FORMULARIO ===")
    for field_name, field in form.fields.items():
        print(f"Campo: {field_name}")
        print(f"  Label: {field.label}")
        print(f"  Widget: {field.widget}")
        print(f"  Widget attrs: {field.widget.attrs}")
        print(f"  ID for label: {field.id_for_label}")
        print("---")

    # Ver HTML renderizado de algunos campos
    print("\n=== HTML RENDERIZADO ===")
    print("first_name:", form['first_name'])
    print("last_name:", form['last_name'])
    print("email:", form['email'])

if __name__ == '__main__':
    test_formulario()
