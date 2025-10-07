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

def test_static_files(request):
    """Vista de prueba para verificar archivos estáticos"""
    return render(request, 'test_static.html', {})

def debug_static_files(request):
    """Página de diagnóstico para archivos estáticos"""
    from django.conf import settings
    return render(request, 'debug_static.html', {
        'DEBUG': settings.DEBUG,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'bootstrap_loaded': True,
    })

def test_logo_view(request):
    """Vista específica para probar el logo Setel"""
    return render(request, 'test_logo.html', {})
