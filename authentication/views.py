from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def test_logout(request):
    """Página de prueba para verificar logout"""
    return HttpResponse("Test logout page - Usuario autenticado: " + str(request.user.is_authenticated))

def test_page(request):
    """Página de prueba simple"""
    return HttpResponse("Test page - Servidor funcionando correctamente")
