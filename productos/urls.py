from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.producto_list, name='list'),
    path('nuevo/', views.producto_create, name='create'),
    path('<int:pk>/', views.producto_detail, name='detail'),
    path('<int:pk>/editar/', views.producto_edit, name='edit'),
    path('<int:pk>/eliminar/', views.producto_delete, name='delete'),
    path('<int:producto_id>/movimiento/', views.movimiento_create, name='movimiento_create'),
]
