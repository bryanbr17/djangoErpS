from django.urls import path
from . import views

app_name = 'configuracion'

urlpatterns = [
    path('', views.configuracion_index, name='index'),
    path('general/', views.configuracion_general, name='general'),
    path('correo/', views.configuracion_correo, name='correo'),
    path('seguridad/', views.configuracion_seguridad, name='seguridad'),
    path('respaldos/', views.configuracion_respaldos, name='respaldos'),
]
