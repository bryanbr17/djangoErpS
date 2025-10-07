from django.urls import path
from . import views

app_name = 'cotizaciones'

urlpatterns = [
    path('', views.cotizacion_list, name='list'),
    path('emitir/', views.cotizacion_create, name='create'),
    path('<int:pk>/', views.cotizacion_detail, name='detail'),
    path('<int:pk>/editar/', views.cotizacion_edit, name='edit'),
    path('<int:pk>/eliminar/', views.cotizacion_delete, name='delete'),
    path('<int:pk>/aprobar/', views.cotizacion_aprobar, name='aprobar'),
    path('<int:pk>/rechazar/', views.cotizacion_rechazar, name='rechazar'),
]
