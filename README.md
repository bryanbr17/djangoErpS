# Sistema ERP - Django

*Sistema integral de gestión empresarial desarrollado con Django y MySQL*

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+ instalado
- XAMPP instalado y ejecutándose (Apache + MySQL)
- Git instalado

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd erp_django
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Iniciar XAMPP**
- Abre el Panel de Control de XAMPP
- Inicia Apache y MySQL
- Verifica que MySQL esté ejecutándose en el puerto 3306

6. **Configurar base de datos**
La base de datos `bryanbr17` ya está configurada en `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bryanbr17',
        'USER': 'root',
        'PASSWORD': '',  # XAMPP por defecto no tiene contraseña
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

7. **Verificar base de datos (opcional)**
Accede a phpMyAdmin en `http://localhost/phpmyadmin` para verificar que la base de datos `bryanbr17` existe.

8. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

9. **Crear superusuario**
```bash
python manage.py createsuperuser
```

10. **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

11. **Abrir en el navegador**
```
http://localhost:8000
```

## 📁 Estructura del Proyecto

```
erp_django/
├── erp_system/           # Configuración principal del proyecto
├── authentication/       # Aplicación de autenticación
├── dashboard/           # Dashboard principal
├── tecnicos/           # Gestión de técnicos
├── cotizaciones/       # Sistema de cotizaciones
├── productos/          # Gestión de productos/inventario
├── reportes/           # Sistema de reportes
├── templates/          # Templates HTML globales
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── media/              # Archivos subidos por usuarios
└── requirements.txt    # Dependencias del proyecto
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.6
- **Base de datos**: MySQL 8.0+
- **Frontend**: Django Templates + Bootstrap 5
- **Estilos**: Bootstrap 5 + CSS personalizado
- **Iconos**: Bootstrap Icons
- **Gráficos**: Chart.js

## 📋 Funcionalidades

### ✅ Implementadas
- 🔐 Sistema de autenticación Django
- 📊 Dashboard con métricas
- 👥 Gestión de técnicos
- 💼 Sistema de cotizaciones
- 🏢 Gestión de inventario/productos
- 📈 Sistema de reportes
- 📱 Diseño responsive con Bootstrap

### 🚧 En desarrollo
- 📧 Sistema de notificaciones
- 📄 Generación de PDFs
- 📊 Reportes avanzados con gráficos
- 🔄 API REST (opcional)

## 🔧 Comandos Útiles

```bash
# Crear nueva aplicación
python manage.py startapp nombre_app

# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Shell de Django
python manage.py shell
```

## 🗄️ Modelos de Base de Datos

### Técnicos
- Información personal
- Especialidades
- Estado (activo/inactivo)
- Documentos adjuntos

### Cotizaciones
- Cliente
- Productos/servicios
- Precios y descuentos
- Estado de la cotización

### Productos
- Información del producto
- Stock disponible
- Precios
- Categorías

### Reportes
- Ventas por período
- Inventario
- Rendimiento de técnicos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ usando Django**
