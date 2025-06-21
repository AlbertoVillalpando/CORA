#!/bin/bash

# CORA Environment Initializer
# Script para inicializar automáticamente el entorno virtual y configuración

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mostrar el banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║     🏛️  CORA - Conference Review Management System           ║"
    echo "║     🔧  Environment Initializer                              ║"
    echo "║     🎓  Universidad Autónoma de Zacatecas                    ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Funciones de logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

log_step() {
    echo -e "\n${CYAN}🔄 $1${NC}"
}

# Función para detectar el OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    log_info "OS detectado: $OS"
}

# Función para verificar requisitos
check_requirements() {
    log_step "Verificando requisitos del sistema..."
    
    # Verificar Python 3
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_success "Python $PYTHON_VERSION encontrado"
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        log_error "pip no está instalado. Por favor instala pip."
    fi
    
    # Verificar git
    if ! command -v git &> /dev/null; then
        log_warning "Git no está instalado. Algunas funciones pueden no estar disponibles."
    fi
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "manage.py" ]; then
        log_error "No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto CORA."
    fi
    
    log_success "Todos los requisitos están satisfechos"
}

# Función para crear entorno virtual
create_virtual_environment() {
    log_step "Configurando entorno virtual..."
    
    if [ -d "venv" ]; then
        log_warning "El entorno virtual ya existe en 'venv/'"
        echo -n "¿Deseas recrearlo? (y/N): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            log_info "Eliminando entorno virtual existente..."
            rm -rf venv
        else
            log_info "Usando entorno virtual existente"
            return 0
        fi
    fi
    
    log_info "Creando nuevo entorno virtual..."
    python3 -m venv venv || log_error "No se pudo crear el entorno virtual"
    log_success "Entorno virtual creado en 'venv/'"
}

# Función para activar entorno virtual
activate_virtual_environment() {
    log_step "Activando entorno virtual..."
    
    if [[ "$OS" == "windows" ]]; then
        source venv/Scripts/activate
        ACTIVATION_SCRIPT="venv/Scripts/activate"
    else
        source venv/bin/activate
        ACTIVATION_SCRIPT="venv/bin/activate"
    fi
    
    # Verificar que está activado
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        log_success "Entorno virtual activado: $VIRTUAL_ENV"
    else
        log_error "No se pudo activar el entorno virtual"
    fi
}

# Función para instalar dependencias
install_dependencies() {
    log_step "Instalando dependencias..."
    
    # Actualizar pip
    log_info "Actualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependencias principales
    log_info "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt || log_error "Error instalando dependencias"
    
    # Verificar instalación crítica
    log_info "Verificando instalación de django-environ..."
    python -c "import environ; print('✅ django-environ instalado correctamente')" || log_error "django-environ no se instaló correctamente"
    
    log_success "Dependencias instaladas correctamente"
}

# Función para configurar variables de entorno
setup_environment_variables() {
    log_step "Configurando variables de entorno..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            log_info "Copiando configuración desde .env.example..."
            cp .env.example .env
            
            # Generar SECRET_KEY segura
            log_info "Generando SECRET_KEY segura..."
            if command -v python &> /dev/null; then
                NEW_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
            else
                NEW_SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
            fi
            
            # Reemplazar SECRET_KEY en .env
            if [[ "$OS" == "macos" ]]; then
                sed -i '' "s/your-secret-key-here/$NEW_SECRET_KEY/g" .env
            else
                sed -i "s/your-secret-key-here/$NEW_SECRET_KEY/g" .env
            fi
            
            log_success "Archivo .env configurado con SECRET_KEY segura"
        else
            log_error "No se encontró .env.example. No se puede configurar el entorno."
        fi
    else
        log_warning "El archivo .env ya existe. No se modificará."
    fi
}

# Función para configurar base de datos
setup_database() {
    log_step "Configurando base de datos..."
    
    # Verificar configuración de Django
    log_info "Verificando configuración de Django..."
    python manage.py check || log_error "La configuración de Django tiene errores"
    
    # Ejecutar migraciones
    log_info "Ejecutando migraciones de base de datos..."
    python manage.py migrate || log_error "Error ejecutando migraciones"
    
    log_success "Base de datos configurada correctamente"
}

# Función para crear directorios necesarios
create_directories() {
    log_step "Creando directorios necesarios..."
    
    # Crear directorio de logs
    mkdir -p logs
    touch logs/django.log
    touch logs/security.log
    chmod 644 logs/*.log
    
    # Crear directorio de backups
    mkdir -p backups
    
    # Crear directorio de media si no existe
    mkdir -p media/conferencias_zips
    
    log_success "Directorios creados correctamente"
}

# Función para verificar instalación
verify_installation() {
    log_step "Verificando instalación..."
    
    # Test de importación de Django
    python -c "import django; print(f'Django {django.get_version()} instalado')" || log_error "Django no funciona correctamente"
    
    # Test de configuración
    python manage.py check --verbosity=0 || log_warning "Hay advertencias en la configuración"
    
    # Test de SECRET_KEY
    python -c "
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cora.settings')
import django
django.setup()
assert settings.SECRET_KEY, 'SECRET_KEY no está configurada'
print('✅ SECRET_KEY configurada correctamente')
" || log_error "SECRET_KEY no está configurada"
    
    log_success "Instalación verificada correctamente"
}

# Función para mostrar información final
show_final_info() {
    echo -e "\n${GREEN}🎉 ¡Entorno inicializado exitosamente!${NC}\n"
    
    echo -e "${CYAN}📋 Resumen de la configuración:${NC}"
    echo -e "   ✅ Entorno virtual: ${YELLOW}venv/${NC}"
    echo -e "   ✅ Dependencias instaladas correctamente"
    echo -e "   ✅ Variables de entorno: ${YELLOW}.env${NC}"
    echo -e "   ✅ Base de datos: ${YELLOW}db.sqlite3${NC}"
    echo -e "   ✅ Logs: ${YELLOW}logs/${NC}"
    echo -e "   ✅ Configuración verificada"
    
    echo -e "\n${CYAN}🚀 Para iniciar el servidor:${NC}"
    if [[ "$OS" == "windows" ]]; then
        echo -e "   ${YELLOW}venv\\Scripts\\activate${NC}"
    else
        echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    fi
    echo -e "   ${YELLOW}python manage.py runserver${NC}"
    
    echo -e "\n${CYAN}🌐 Luego visita:${NC}"
    echo -e "   🏠 Aplicación: ${YELLOW}http://localhost:8000${NC}"
    echo -e "   👮 Admin: ${YELLOW}http://localhost:8000/admin${NC}"
    
    echo -e "\n${CYAN}📚 Documentación:${NC}"
    echo -e "   📖 Instalación completa: ${YELLOW}INSTALACION_SEGURA.md${NC}"
    echo -e "   🔧 Configuración: ${YELLOW}CLAUDE.md${NC}"
    
    echo -e "\n${CYAN}🔧 Comandos útiles:${NC}"
    echo -e "   🧪 Ejecutar tests: ${YELLOW}python manage.py test${NC}"
    echo -e "   🔒 Verificar seguridad: ${YELLOW}python manage.py check --deploy${NC}"
    echo -e "   📊 Ver logs: ${YELLOW}tail -f logs/django.log${NC}"
    
    if [[ "$OS" == "windows" ]]; then
        echo -e "\n${YELLOW}💡 Para reactivar el entorno en el futuro:${NC}"
        echo -e "   ${YELLOW}venv\\Scripts\\activate${NC}"
    else
        echo -e "\n${YELLOW}💡 Para reactivar el entorno en el futuro:${NC}"
        echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    fi
}

# Función para manejar errores
handle_error() {
    log_error "El script falló en el paso: $1"
}

# Función principal
main() {
    # Mostrar banner
    show_banner
    
    # Detectar OS
    detect_os
    
    # Configurar trap para errores
    trap 'handle_error "$(caller)"' ERR
    
    # Ejecutar pasos
    check_requirements
    create_virtual_environment
    activate_virtual_environment
    install_dependencies
    setup_environment_variables
    create_directories
    setup_database
    verify_installation
    show_final_info
    
    echo -e "\n${GREEN}✨ ¡Inicialización completada exitosamente! ✨${NC}"
}

# Función de ayuda
show_help() {
    echo "CORA Environment Initializer"
    echo ""
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -v, --verbose  Modo verboso"
    echo "  --skip-venv    Saltar creación de entorno virtual"
    echo "  --skip-deps    Saltar instalación de dependencias"
    echo "  --skip-db      Saltar configuración de base de datos"
    echo ""
    echo "Ejemplos:"
    echo "  $0              Inicialización completa"
    echo "  $0 --skip-venv  Inicializar sin crear entorno virtual"
    echo ""
}

# Procesamiento de argumentos
SKIP_VENV=false
SKIP_DEPS=false
SKIP_DB=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --skip-db)
            SKIP_DB=true
            shift
            ;;
        *)
            echo "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Ejecutar función principal
main "$@"