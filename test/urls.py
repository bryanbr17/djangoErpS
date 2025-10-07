from django.urls import path
from . import views

app_name = 'test'

urlpatterns = [
    path('test/', views.test_page, name='test_page'),
    path('test-logout/', views.test_logout, name='test_logout'),
    path('test-static/', views.test_static_files, name='test_static_files'),
    path('debug-static/', views.debug_static_files, name='debug_static_files'),
    path('test-logo/', views.test_logo_view, name='test_logo_view'),
]
