"""
URL configuration for erp_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard:index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('auth/', include('authentication.urls')),
    path('tecnicos/', include('tecnicos.urls')),
    path('productos/', include('productos.urls')),
    path('cotizaciones/', include('cotizaciones.urls')),
    path('reportes/', include('reportes.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('test/', include('test.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
