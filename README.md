# CORA - Conference Review Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Coverage](https://img.shields.io/badge/Coverage-95%25+-brightgreen.svg)](https://coverage.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

CORA es un sistema de gestión de revisión de conferencias académicas, similar a EasyChair, que permite gestionar el proceso completo de revisión de trabajos académicos desde la submisión hasta la evaluación final.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación Rápida](#-instalación-rápida)
- [Instalación Manual](#-instalación-manual)
- [Uso](#-uso)
- [Testing](#-testing)
- [Arquitectura](#-arquitectura)
- [Contribuir](#-contribuir)
- [Documentación](#-documentación)
- [Soporte](#-soporte)

## ✨ Características

- **Gestión de Usuarios**: Sistema de autenticación con roles (Admin, Organizador, Autor, Revisor)
- **Gestión de Conferencias**: Creación y administración de conferencias académicas
- **Sistema de Invitaciones**: Invitación automática de revisores por área de conocimiento
- **Evaluación Dinámica**: Formularios de evaluación personalizables con sistema de puntuación 1-5
- **Gestión de Archivos**: Subida de trabajos en formato ZIP con validación
- **Notificaciones**: Sistema de alertas en tiempo real para todos los usuarios
- **Dashboard Personalizado**: Interfaces específicas para cada tipo de usuario
- **Reportes**: Generación de reportes de evaluación y estadísticas

## 🛠️ Tecnologías

### Backend
- **Django 4.2+** - Framework web principal
- **Python 3.8+** - Lenguaje de programación
- **SQLite/MariaDB** - Base de datos (desarrollo/producción)
- **Django REST Framework** - API REST (opcional)

### Frontend
- **Bootstrap 5** - Framework CSS
- **jQuery** - Biblioteca JavaScript
- **HTML5/CSS3** - Tecnologías web estándar

### Testing & QA
- **Django Test Framework** - Tests unitarios
- **Behave + Selenium** - Tests de aceptación BDD
- **Coverage.py** - Cobertura de código (95% mínimo)
- **Flake8** - Linting de código

### DevOps
- **Docker & Docker Compose** - Containerización
- **GitHub Actions** - CI/CD (opcional)
- **Gunicorn** - Servidor WSGI para producción

## ⚡ Instalación Rápida

### Opción 1: Script Automático (Recomendado)

```bash
# Linux/MacOS
chmod +x init-env.sh
./init-env.sh

# Windows
init-env.bat
```

Después de ejecutar el script:
```bash
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

python manage.py runserver
```

### Opción 2: Docker (Recomendado para Desarrollo)

```bash
# Crear red de Docker
docker network create proxy

# Levantar servicios
docker-compose up -d --build

# Acceder a http://localhost:8000
```

## 🔧 Instalación Manual

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Docker y Docker Compose (opcional)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/easy-chair-uaz.git
cd easy-chair-uaz
```

2. **Crear y activar entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario** (opcional)
```bash
python manage.py createsuperuser
```

7. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

La aplicación estará disponible en http://localhost:8000

## 🚀 Uso

### Acceso al Sistema

- **URL Principal**: http://localhost:8000
- **Panel de Administración**: http://localhost:8000/admin

### Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| `adminP@adminP.com` | `P123456789` | Administrador |
| `organizadorP@organizadorP.com` | `P123456789` | Organizador |
| `autorP@autorP.com` | `P123456789` | Autor |
| `revisorP@revisorP.com` | `P123456789` | Revisor |

### Flujo de Trabajo Principal

1. **Organizador**: Crea una conferencia y define formulario de evaluación
2. **Organizador**: Invita revisores por área de conocimiento
3. **Autor**: Sube trabajo académico en formato ZIP
4. **Revisor**: Acepta invitación y evalúa trabajo asignado
5. **Organizador**: Revisa evaluaciones y toma decisión final
6. **Sistema**: Notifica resultados a todos los participantes

## 🧪 Testing

### Ejecutar Tests Completos

```bash
# Tests con cobertura (mínimo 95%)
coverage run --branch --source='.' --omit="*/migrations/*,*test*,*__init__*,*settings*,*apps*,*wsgi.py*,*admin.py*,*asgi.py*,*manage.py*,*urls.py*" manage.py test

# Generar reporte de cobertura
coverage report -m --fail-under 95

# Generar reporte HTML
coverage html
```

### Tests por Aplicación

```bash
# Tests de usuarios
python manage.py test usuarios

# Tests de conferencias
python manage.py test conferencia

# Tests de formularios
python manage.py test formulario

# Tests de notificaciones
python manage.py test notificaciones
```

### Tests de Aceptación (BDD)

```bash
# Todos los tests BDD
behave pruebas_aceptacion/CORA/features/

# Test específico
behave pruebas_aceptacion/CORA/features/cu1_inicio_sesion.feature
```

### Verificar Calidad de Código

```bash
# Linting
flake8 .

# Verificar configuración Django
python manage.py check

# Verificar configuración para producción
python manage.py check --deploy
```

## 🏗️ Arquitectura

### Estructura del Proyecto

```
cora/
├── cora/                    # Configuración Django principal
├── usuarios/                # Gestión de usuarios y autenticación
├── conferencia/             # Gestión de conferencias y trabajos
├── formulario/              # Sistema de evaluación dinámico
├── notificaciones/          # Sistema de alertas
├── home/                    # Página principal y dashboards
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── media/                   # Archivos subidos por usuarios
├── templates/               # Templates HTML base
└── pruebas_aceptacion/      # Tests BDD con Behave
```

### Modelos Principales

- **CustomUser**: Usuario con email como identificador y áreas de conocimiento
- **Conferencia**: Trabajos académicos con archivos ZIP y metadatos
- **InvitacionRevisor**: Sistema de invitaciones con estados (pendiente/aceptado/rechazado)
- **Evaluacion/Pregunta/Respuesta**: Sistema de evaluación dinámico
- **Notificacion**: Alertas del sistema para usuarios

### Roles y Permisos

| Rol | Crear Conferencia | Invitar Revisores | Subir Trabajos | Evaluar Trabajos |
|-----|------------------|-------------------|----------------|------------------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| Organizador | ✅ | ✅ (propias) | ❌ | ❌ |
| Autor | ❌ | ❌ | ✅ (propias) | ❌ |
| Revisor | ❌ | ❌ | ❌ | ✅ (asignadas) |

## 🤝 Contribuir

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama para nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
3. Realizar cambios y escribir tests
4. Verificar cobertura de tests (95% mínimo)
5. Hacer commit siguiendo [Conventional Commits](https://www.conventionalcommits.org/)
6. Push de la rama: `git push origin feature/nueva-funcionalidad`
7. Crear Pull Request

### Estándares de Código

- Seguir PEP 8 para Python
- Cobertura de tests mínima del 95%
- Documentar funciones y clases importantes
- Usar nombres descriptivos para variables y funciones
- Seguir patrones de Django (models, views, templates)

### Comandos de Desarrollo

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell de Django
python manage.py shell

# Colectar archivos estáticos
python manage.py collectstatic

# Crear fixture de datos
python manage.py dumpdata app.Model --indent 2 > fixtures/data.json
```

## 📚 Documentación

- **[CLAUDE.md](CLAUDE.md)** - Comandos y configuración para Claude Code
- **[GUIA_DESARROLLADOR.md](GUIA_DESARROLLADOR.md)** - Guía completa para desarrolladores
- **[README-ENTORNO.md](README-ENTORNO.md)** - Configuración automática del entorno
- **[ANALISIS_PROYECTO.md](ANALISIS_PROYECTO.md)** - Análisis técnico del proyecto

## 🚀 Despliegue en Producción

### Docker (Recomendado)

```bash
# Usar archivo de producción
docker-compose -f docker-compose.prod.yml up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Colectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Variables de Entorno de Producción

```bash
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=mysql://usuario:password@localhost/cora_db
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

## 🆘 Soporte

### Obtener Ayuda

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/easy-chair-uaz/issues)
- **Documentación**: Ver archivos de documentación en el repositorio

### Problemas Comunes

**Error de migraciones:**
```bash
python manage.py migrate --fake-initial
```

**Error de permisos en archivos:**
```bash
chmod +x init-env.sh
```

**Error de dependencias:**
```bash
pip install -r requirements.txt --upgrade
```

### Estado del Proyecto

- ✅ Sistema base funcional
- ✅ Autenticación y roles
- ✅ Gestión de conferencias
- ✅ Sistema de evaluación
- ✅ Tests automatizados (95%+ cobertura)
- 🔄 Mejoras de UI/UX en desarrollo
- 🔄 API REST en desarrollo
- 📋 Notificaciones por email planificadas

---

**Desarrollado con ❤️ para la comunidad académica**

*Para más información, consulta la [documentación completa](GUIA_DESARROLLADOR.md) o los archivos de configuración específicos.*
