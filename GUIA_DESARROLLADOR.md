# Guía del Desarrollador - CORA
## Sistema de Gestión de Revisión de Conferencias Académicas

**¡Bienvenido/a al equipo de desarrollo de CORA!** 🎉

Esta guía te ayudará a familiarizarte rápidamente con el proyecto y comenzar a contribuir de manera efectiva.

---

## 📖 Índice

1. [Introducción al Sistema](#introducción-al-sistema)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
4. [Flujo de Trabajo del Sistema](#flujo-de-trabajo-del-sistema)
5. [Guía de Código](#guía-de-código)
6. [Testing y Calidad](#testing-y-calidad)
7. [Workflow de Desarrollo](#workflow-de-desarrollo)
8. [Recursos y Referencias](#recursos-y-referencias)

---

## 🎯 Introducción al Sistema

### ¿Qué es CORA?

CORA (Conference Review Management System) es una plataforma web que gestiona el proceso completo de revisión de conferencias académicas, similar a sistemas como EasyChair. Permite a organizadores, autores y revisores colaborar en el proceso de evaluación de trabajos académicos.

### Problema que Resuelve

- **Gestión manual ineficiente** de revisiones académicas
- **Falta de trazabilidad** en el proceso de evaluación
- **Comunicación fragmentada** entre participantes
- **Ausencia de estándares** en la evaluación

### Usuarios del Sistema

| Rol | Responsabilidades |
|-----|-------------------|
| **Administrador** | Supervisión general, gestión de usuarios, estadísticas |
| **Organizador** | Crear conferencias, invitar revisores, gestionar proceso |
| **Autor** | Subir trabajos, consultar estado de evaluación |
| **Revisor** | Evaluar trabajos asignados, proporcionar retroalimentación |

---

## ⚙️ Configuración del Entorno

### Requisitos Previos

- **Python 3.8+**
- **Git**
- **Docker & Docker Compose** (recomendado)
- **Editor de código** (VS Code, PyCharm, etc.)

### Setup Rápido

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-repo/easy-chair-uaz.git
cd easy-chair-uaz
```

2. **Configurar entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements-dev.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones locales
```

5. **Ejecutar migraciones:**
```bash
python manage.py migrate
```

6. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

7. **Cargar datos de prueba:**
```bash
python manage.py loaddata fixtures/test_users.json
```

8. **Ejecutar servidor de desarrollo:**
```bash
python manage.py runserver
```

### Setup con Docker (Recomendado)

```bash
# Crear red de Docker
docker network create proxy

# Levantar servicios
docker-compose up -d --build

# Acceder en http://localhost:8000
```

### Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| `adminP@adminP.com` | `P123456789` | Administrador |
| `organizadorP@organizadorP.com` | `P123456789` | Organizador |
| `autorP@autorP.com` | `P123456789` | Autor |
| `revisorP@revisorP.com` | `P123456789` | Revisor |

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
easy-chair-uaz/
├── cora/                    # Configuración principal Django
│   ├── settings.py         # Configuraciones del proyecto
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI para producción
├── usuarios/              # 👥 Gestión de usuarios y autenticación
│   ├── models.py          # CustomUser, roles
│   ├── views.py           # Login, registro, dashboards
│   ├── forms.py           # Formularios de autenticación
│   └── templates/         # Templates de usuario
├── conferencia/           # 📋 Gestión de conferencias
│   ├── models.py          # Conferencia, InvitacionRevisor
│   ├── views.py           # CRUD conferencias, invitaciones
│   ├── forms.py           # Formularios de conferencia
│   └── templates/         # Templates de conferencia
├── formulario/            # 📝 Sistema de evaluación
│   ├── models.py          # Evaluacion, Pregunta, Respuesta
│   ├── views.py           # Crear/evaluar formularios
│   └── templates/         # Templates de evaluación
├── notificaciones/        # 🔔 Sistema de alertas
│   ├── models.py          # Notificacion
│   ├── views.py           # Dropdown, marcar leídas
│   └── context_processors.py # Contexto global
├── home/                  # 🏠 Página principal y dashboards
├── static/                # 🎨 Archivos estáticos (CSS, JS, imágenes)
├── media/                 # 📁 Archivos subidos por usuarios
├── templates/             # 📄 Templates base
└── requirements.txt       # 📦 Dependencias Python
```

### Apps Django y Sus Responsabilidades

#### 🔐 `usuarios` - Autenticación y Roles
- **Modelo principal:** `CustomUser`
- **Características:**
  - Email como username
  - Áreas de conocimiento (Ingeniería, Medicina, Letras, Contabilidad)
  - Sistema de roles integrado con Django Groups
  - Password reset personalizado

#### 📋 `conferencia` - Gestión de Conferencias
- **Modelos principales:** `Conferencia`, `InvitacionRevisor`
- **Características:**
  - Upload de archivos ZIP
  - Sistema de invitaciones a revisores
  - Estados de revisión (aceptado/rechazado)
  - Relaciones organizador-autor-revisor

#### 📝 `formulario` - Sistema de Evaluación
- **Modelos principales:** `Evaluacion`, `Pregunta`, `Respuesta`
- **Características:**
  - Formularios dinámicos por conferencia
  - Sistema de puntuación 1-5
  - Retroalimentación textual
  - Restricción: un revisor = una evaluación por conferencia

#### 🔔 `notificaciones` - Sistema de Alertas
- **Modelo principal:** `Notificacion`
- **Características:**
  - Notificaciones en tiempo real
  - Dropdown de alertas
  - Marcado masivo como leídas
  - Context processor global

---

## 🔄 Flujo de Trabajo del Sistema

### 1. Flujo Principal de Revisión

```mermaid
graph TD
    A[Organizador crea conferencia] --> B[Organizador invita revisores]
    B --> C[Autor sube trabajo ZIP]
    C --> D[Revisores reciben invitación]
    D --> E{Revisor acepta?}
    E -->|Sí| F[Revisor evalúa trabajo]
    E -->|No| G[Invitación rechazada]
    F --> H[Organizador ve evaluaciones]
    H --> I[Decisión final: Aceptado/Rechazado]
    I --> J[Autor recibe notificación]
```

### 2. Estados de una Conferencia

```mermaid
stateDiagram-v2
    [*] --> Creada
    Creada --> ConArchivo: Autor sube ZIP
    ConArchivo --> EnRevision: Revisores invitados
    EnRevision --> Evaluada: Evaluaciones completadas
    Evaluada --> Aceptada: Decisión positiva
    Evaluada --> Rechazada: Decisión negativa
    Aceptada --> [*]
    Rechazada --> [*]
```

### 3. Roles y Permisos

| Acción | Admin | Organizador | Autor | Revisor |
|--------|-------|-------------|-------|---------|
| Ver todas las conferencias | ✅ | ❌ | ❌ | ❌ |
| Crear conferencia | ✅ | ✅ | ❌ | ❌ |
| Invitar revisores | ✅ | ✅ (propias) | ❌ | ❌ |
| Subir trabajos | ✅ | ❌ | ✅ (propias) | ❌ |
| Evaluar trabajos | ✅ | ❌ | ❌ | ✅ (asignadas) |
| Descargar archivos | ✅ | ✅ (propias) | ✅ (propias) | ✅ (asignadas) |

---

## 💻 Guía de Código

### Convenciones de Naming

```python
# Modelos: PascalCase
class Conferencia(models.Model):
    pass

# Variables y funciones: snake_case
def crear_conferencia_view(request):
    conference_name = request.POST.get('nombre')

# Constantes: UPPER_SNAKE_CASE
AREAS_CONOCIMIENTO = [
    ('Ingenieria', 'Ingeniería'),
    ('Medicina', 'Medicina'),
]

# Templates: kebab-case
'conferencia/conferencias-administrador.html'

# URLs: kebab-case con guiones bajos para parámetros
path('conferencias/<int:conferencia_id>/evaluar/', ...)
```

### Estructura de Vistas Típica

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

@login_required
def ejemplo_vista(request, conferencia_id):
    """
    Docstring explicando qué hace la vista.
    
    Args:
        request: HttpRequest object
        conferencia_id: ID de la conferencia
        
    Returns:
        HttpResponse: Renderiza template o redirecciona
    """
    # 1. Obtener objetos necesarios
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    
    # 2. Verificar permisos
    if not conferencia.puede_acceder(request.user):
        messages.error(request, 'No tienes permisos para esta acción')
        return redirect('home')
    
    # 3. Procesar POST
    if request.method == 'POST':
        # Lógica de procesamiento
        try:
            # ... lógica ...
            messages.success(request, 'Operación exitosa')
            return redirect('success_url')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # 4. Preparar contexto
    context = {
        'conferencia': conferencia,
        'can_edit': conferencia.puede_editar(request.user),
    }
    
    # 5. Renderizar template
    return render(request, 'conferencia/ejemplo.html', context)
```

### Patrones de Modelos

```python
class MiModelo(models.Model):
    """Docstring del modelo"""
    
    # 1. Campos del modelo
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # 2. Meta class
    class Meta:
        verbose_name = 'Mi Modelo'
        verbose_name_plural = 'Mis Modelos'
        ordering = ['-fecha_creacion']
    
    # 3. Métodos especiales
    def __str__(self):
        return self.nombre
    
    # 4. Métodos de validación
    def clean(self):
        if self.nombre and len(self.nombre) < 3:
            raise ValidationError('Nombre muy corto')
    
    # 5. Métodos de negocio
    def puede_ser_editado(self, usuario):
        return self.creador == usuario or usuario.is_staff
    
    # 6. Properties
    @property
    def esta_activo(self):
        return self.estado == 'activo'
```

### Template Patterns

```html
<!-- Usar herencia de templates -->
{% extends 'base.html' %}

<!-- Cargar tags necesarios -->
{% load static %}

<!-- Definir bloques -->
{% block title %}Mi Página{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Mostrar mensajes -->
    {% if messages %}
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    {% endif %}
    
    <!-- Verificar permisos en template -->
    {% if user.is_authenticated and conferencia.puede_editar %}
        <a href="{% url 'editar_conferencia' conferencia.id %}" class="btn btn-primary">
            Editar
        </a>
    {% endif %}
    
    <!-- Iterar con empty -->
    {% for item in lista %}
        <p>{{ item.nombre }}</p>
    {% empty %}
        <p>No hay elementos disponibles.</p>
    {% endfor %}
</div>
{% endblock %}
```

---

## 🧪 Testing y Calidad

### Cobertura de Tests

El proyecto mantiene **95% de cobertura mínima**. Los tests están organizados por app:

```
app/tests/
├── __init__.py
├── test_models.py      # Tests de modelos
├── test_views.py       # Tests de vistas
├── test_forms.py       # Tests de formularios
└── test_utils.py       # Tests de utilidades
```

### Ejecutar Tests

```bash
# Tests completos con cobertura
coverage run --branch --source='.' --omit="*/migrations/*,*test*,*__init__*,*settings*,*apps*,*wsgi.py*,*admin.py*,*asgi.py*,*manage.py*,*urls.py*" manage.py test

# Reporte de cobertura
coverage report -m --fail-under 95

# Reporte HTML
coverage html

# Tests de una app específica
python manage.py test usuarios

# Test específico
python manage.py test usuarios.tests.test_models.CustomUserTestCase.test_user_creation
```

### Ejemplo de Test

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from conferencia.models import Conferencia

User = get_user_model()

class ConferenciaViewTestCase(TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='testpass123',
            nombre='Test',
            apellidos='User',
            area_conocimiento='Ingenieria'
        )
        
    def test_crear_conferencia_requiere_login(self):
        """Test que crear conferencia requiere autenticación"""
        url = reverse('crear_conferencia')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_crear_conferencia_exitosa(self):
        """Test creación exitosa de conferencia"""
        self.client.login(username='test@test.com', password='testpass123')
        
        data = {
            'nombre': 'Mi Conferencia de Prueba',
            'categoria': 'Ingenieria',
            'meses': 0,
            'dias': 5,
            'horas': 0,
            'minutos': 0,
        }
        
        response = self.client.post(reverse('crear_conferencia'), data)
        
        self.assertEqual(response.status_code, 302)  # Redirect después de crear
        self.assertTrue(
            Conferencia.objects.filter(nombre='Mi Conferencia de Prueba').exists()
        )
```

### Tests BDD (Behave)

```bash
# Ejecutar tests de aceptación
behave pruebas_aceptacion/CORA/features/

# Test específico
behave pruebas_aceptacion/CORA/features/cu1_inicio_sesion.feature
```

### Linting

```bash
# Verificar estilo de código
flake8 .

# Configuración en setup.cfg
[flake8]
max-line-length = 88
exclude = migrations, venv, __pycache__
```

---

## 🔄 Workflow de Desarrollo

### Git Flow

```bash
# 1. Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios y commits descriptivos
git add .
git commit -m "feat: agregar sistema de notificaciones por email

- Implementar backend SMTP
- Crear templates de email
- Agregar tests de integración

Fixes #123"

# 3. Ejecutar tests antes de push
python manage.py test
coverage run manage.py test && coverage report --fail-under=95

# 4. Push de la rama
git push origin feature/nueva-funcionalidad

# 5. Crear Pull Request
# 6. Code review
# 7. Merge a main
```

### Formato de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(scope): descripción corta

Descripción más detallada si es necesaria.

- Punto específico 1
- Punto específico 2

Fixes #123
Closes #456
```

**Tipos de commit:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formateo de código
- `refactor`: Refactoring
- `test`: Agregar tests
- `chore`: Tareas de mantenimiento

### Revisión de Código

**Checklist para PRs:**
- [ ] Tests pasan (95% cobertura mínima)
- [ ] Código sigue convenciones del proyecto
- [ ] Documentación actualizada
- [ ] Sin secrets hardcodeados
- [ ] Migraciones incluidas si es necesario
- [ ] Templates actualizados si es necesario

---

## 🛠️ Herramientas de Desarrollo

### Debugging

```python
# En development settings
DEBUG = True

# Para debugging en vistas
import pdb; pdb.set_trace()

# O usar logging
import logging
logger = logging.getLogger(__name__)
logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
```

### Django Debug Toolbar (Recomendado)

```bash
pip install django-debug-toolbar

# En settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Comandos Útiles

```bash
# Gestión de base de datos
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate app_name migration_name

# Shell interactivo
python manage.py shell
python manage.py shell_plus  # Si tienes django-extensions

# Colectar archivos estáticos
python manage.py collectstatic

# Crear fixture
python manage.py dumpdata usuarios.CustomUser --indent 2 > fixtures/users.json

# Cargar fixture
python manage.py loaddata fixtures/users.json

# Verificar configuración
python manage.py check
python manage.py check --deploy  # Para producción
```

---

## 📊 Base de Datos

### Modelo de Datos Principal

```mermaid
erDiagram
    CustomUser ||--o{ Conferencia : "organiza"
    CustomUser ||--o{ Conferencia : "es_autor"
    CustomUser ||--o{ InvitacionRevisor : "recibe"
    CustomUser ||--o{ Evaluacion : "realiza"
    CustomUser ||--o{ Notificacion : "recibe"
    
    Conferencia ||--o{ InvitacionRevisor : "tiene"
    Conferencia ||--o{ Evaluacion : "es_evaluada"
    Conferencia ||--o{ Pregunta : "tiene"
    
    Evaluacion ||--o{ Respuesta : "contiene"
    Pregunta ||--o{ Respuesta : "es_respondida"
    
    CustomUser {
        int id PK
        string email UK
        string username UK
        string nombre
        string apellidos
        string area_conocimiento
        boolean is_staff
        datetime date_joined
    }
    
    Conferencia {
        int id PK
        string nombre
        int organizador_id FK
        int autor_id FK
        string categoria
        string estado_revision
        boolean trabajo_reportado
        file archivo_zip
        int meses
        int dias
        int horas
        int minutos
    }
    
    InvitacionRevisor {
        int id PK
        int conferencia_id FK
        int autor_id FK
        string estado
        datetime fecha_envio
    }
    
    Evaluacion {
        int id PK
        int conferencia_id FK
        int revisor_id FK
        text retroalimentacion
    }
    
    Pregunta {
        int id PK
        int conferencia_id FK
        string texto
    }
    
    Respuesta {
        int id PK
        int evaluacion_id FK
        int pregunta_id FK
        int puntaje
    }
    
    Notificacion {
        int id PK
        int usuario_id FK
        string mensaje
        boolean leida
        datetime fecha
    }
```

### Queries Comunes

```python
# Obtener conferencias de un organizador
conferencias = Conferencia.objects.filter(organizador=user)

# Obtener invitaciones pendientes de un revisor
invitaciones = InvitacionRevisor.objects.filter(
    autor=user, 
    estado='pendiente'
)

# Obtener conferencias que un revisor puede evaluar
conferencias_revisor = Conferencia.objects.filter(
    invitaciones_revisor__autor=user,
    invitaciones_revisor__estado='aceptado'
)

# Optimizar queries con select_related
conferencias = Conferencia.objects.select_related(
    'organizador', 'autor'
).prefetch_related('invitaciones_revisor')

# Obtener evaluaciones de una conferencia
evaluaciones = Evaluacion.objects.filter(
    conferencia=conferencia
).select_related('revisor').prefetch_related('respuestas__pregunta')
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# .env para desarrollo
SECRET_KEY=tu-secret-key-local
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# .env.production para producción
SECRET_KEY=secret-key-super-segura
DEBUG=False
DATABASE_URL=mysql://user:pass@localhost/cora_db
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=cora@tudominio.com
EMAIL_HOST_PASSWORD=app-password
```

### Configuración de Logging

```python
# En settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'usuarios': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

## 🚀 Despliegue

### Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cora.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./media:/app/media
      - ./logs:/app/logs
    env_file:
      - .env.production
    depends_on:
      - db

  db:
    image: mariadb:10.6
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: cora_db
      MYSQL_USER: cora_user
      MYSQL_PASSWORD: cora_pass
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Comandos de Despliegue

```bash
# Construcción
docker-compose build

# Despliegue
docker-compose up -d

# Migraciones en producción
docker-compose exec web python manage.py migrate

# Colectar estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Ver logs
docker-compose logs -f web
```

---

## 🎯 Tareas Comunes para Nuevos Desarrolladores

### Primera Semana

1. **Setup del entorno** (Día 1)
   - Configurar entorno de desarrollo
   - Ejecutar todos los tests
   - Explorar la aplicación con usuarios de prueba

2. **Familiarización con el código** (Días 2-3)
   - Leer esta documentación completa
   - Revisar modelos principales
   - Entender flujo de autenticación

3. **Primera contribución** (Días 4-5)
   - Elegir issue marcado como "good first issue"
   - Hacer fork, crear rama, implementar, tests, PR
   - Participar en code review

### Tareas de Ejemplo para Practicar

#### 🟢 Fácil
- Agregar validación adicional a formularios
- Mejorar mensajes de error
- Agregar campos adicionales a modelos existentes
- Escribir tests para casos edge

#### 🟡 Intermedio
- Implementar nueva funcionalidad de notificaciones
- Agregar sistema de búsqueda
- Implementar paginación en listados
- Crear nuevos endpoints de API

#### 🔴 Avanzado
- Optimizar queries de base de datos
- Implementar sistema de cacheo
- Agregar autenticación con OAuth
- Implementar real-time notifications con WebSockets

---

## 📚 Recursos y Referencias

### Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Herramientas Útiles

- **Django Extensions**: `pip install django-extensions`
- **Django Debug Toolbar**: `pip install django-debug-toolbar`
- **Factory Boy**: Para crear fixtures de test más fácilmente
- **Pillow**: Para manejo de imágenes
- **django-environ**: Para manejo de variables de entorno

### APIs y Librerías Usadas

- **Bootstrap 5**: Framework CSS
- **jQuery**: Para interacciones JavaScript
- **Font Awesome**: Iconos
- **Chart.js**: Gráficos (si se implementa)

### Documentación del Proyecto

- `CLAUDE.md` - Comandos y configuración principal
- `ANALISIS_PROYECTO.md` - Análisis técnico completo
- `PLAN_*.md` - Planes de desarrollo específicos
- `README.md` - Información básica del proyecto

---

## 🆘 Obtener Ayuda

### Canales de Comunicación

1. **Issues en GitHub**: Para bugs y features
2. **Documentación**: Esta guía y CLAUDE.md
3. **Code Review**: En Pull Requests
4. **Slack/Discord**: Canal del equipo (si aplica)

### Preguntas Frecuentes

**Q: ¿Por qué mi migración falla?**
A: Verifica que tengas los últimos cambios de main y que no haya conflictos en migraciones.

**Q: ¿Los tests fallan localmente?**
A: Asegúrate de tener la base de datos limpia: `python manage.py flush --noinput`

**Q: ¿Cómo debuggeo una vista?**
A: Usa `import pdb; pdb.set_trace()` o Django Debug Toolbar.

**Q: ¿Dónde está la configuración de email?**
A: En `settings.py` y variables de entorno. Revisa `PLAN_2_CONFIGURAR_EMAIL_BACKEND.md`

---

## 🎉 ¡Listo para Contribuir!

¡Felicidades! Ahora tienes todo lo necesario para empezar a contribuir efectivamente al proyecto CORA. 

**Próximos pasos:**
1. Configura tu entorno de desarrollo
2. Ejecuta los tests para asegurarte de que todo funciona
3. Elige tu primera tarea del backlog
4. ¡Empieza a codear!

**Recuerda:**
- Siempre hacer tests antes de hacer PR
- Seguir las convenciones de código del proyecto
- Documentar cambios importantes
- Pedir ayuda cuando la necesites

¡Bienvenido/a al equipo! 🚀