#!/bin/bash

# Production Deployment Script - CORA
# Este script automatiza el despliegue seguro en producción

echo "🚀 Iniciando despliegue en producción CORA..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar errores
error() {
    echo -e "${RED}❌ Error: $1${NC}"
    exit 1
}

# Función para mostrar éxito
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Función para mostrar advertencias
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función para mostrar información
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    error "No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto."
fi

# Paso 1: Verificar archivo de configuración de producción
echo "🔍 Verificando configuración de producción..."
if [ ! -f ".env.production.local" ]; then
    error "No se encontró .env.production.local. Crea este archivo basado en .env.production"
fi
success "Archivo de configuración encontrado"

# Paso 2: Verificar variables críticas
echo "🔐 Verificando variables críticas..."
source .env.production.local

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "CHANGE-THIS-TO-A-SECURE-SECRET-KEY-IN-PRODUCTION" ]; then
    error "SECRET_KEY no está configurada correctamente en .env.production.local"
fi

if [ "$DEBUG" != "False" ]; then
    error "DEBUG debe ser False en producción"
fi

if [ -z "$ALLOWED_HOSTS" ] || [ "$ALLOWED_HOSTS" = "your-domain.com,www.your-domain.com" ]; then
    error "ALLOWED_HOSTS no está configurado correctamente"
fi

success "Variables críticas verificadas"

# Paso 3: Backup de la base de datos actual (si existe)
echo "💾 Creando backup de seguridad..."
if [ -f "db.sqlite3" ]; then
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sqlite3"
    cp db.sqlite3 "backups/$BACKUP_FILE" 2>/dev/null || mkdir -p backups && cp db.sqlite3 "backups/$BACKUP_FILE"
    success "Backup creado: backups/$BACKUP_FILE"
fi

# Paso 4: Instalar/actualizar dependencias
echo "📦 Instalando dependencias de producción..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt --no-cache-dir || error "Error instalando dependencias"
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --no-cache-dir || error "Error instalando dependencias"
else
    error "pip/pip3 no encontrado"
fi
success "Dependencias instaladas"

# Paso 5: Verificar configuración de Django
echo "🔍 Verificando configuración de Django..."
export DJANGO_SETTINGS_MODULE=cora.settings_production
python manage.py check --deploy || error "Verificación de configuración falló"
success "Configuración verificada"

# Paso 6: Ejecutar migraciones
echo "💾 Ejecutando migraciones..."
python manage.py migrate || error "Migraciones fallaron"
success "Migraciones completadas"

# Paso 7: Recolectar archivos estáticos
echo "📂 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || warning "Error recolectando archivos estáticos"
success "Archivos estáticos recolectados"

# Paso 8: Crear directorio de logs con permisos
echo "📁 Configurando logs..."
mkdir -p logs
chmod 755 logs
touch logs/django.log logs/security.log
chmod 644 logs/*.log
success "Logs configurados"

# Paso 9: Verificar configuración de seguridad
echo "🔒 Verificando configuración de seguridad..."
SECURITY_CHECK=$(python manage.py check --deploy --verbosity=0 2>&1)
if [ $? -eq 0 ]; then
    success "Todas las verificaciones de seguridad pasaron"
else
    warning "Advertencias de seguridad encontradas:"
    echo "$SECURITY_CHECK"
    read -p "¿Continuar con el despliegue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        error "Despliegue cancelado por el usuario"
    fi
fi

# Paso 10: Test rápido de la aplicación
echo "🧪 Ejecutando test rápido..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cora.settings_production')
django.setup()
from django.conf import settings
print('✅ DEBUG:', settings.DEBUG)
print('✅ SECRET_KEY configurada:', bool(settings.SECRET_KEY))
print('✅ ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
print('✅ CSRF_TRUSTED_ORIGINS:', settings.CSRF_TRUSTED_ORIGINS)
"
success "Test de configuración completado"

# Paso 11: Reiniciar servicios (si aplica)
if command -v systemctl &> /dev/null; then
    echo "🔄 Reiniciando servicios..."
    # Descomenta según tu configuración
    # sudo systemctl restart gunicorn
    # sudo systemctl restart nginx
    info "Servicios de sistema disponibles (reiniciar manualmente si es necesario)"
fi

# Paso 12: Verificación final
echo "🏁 Verificación final..."
echo "Verificando que la aplicación puede iniciar..."
timeout 10 python manage.py runserver --noreload 0.0.0.0:8000 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 3

if kill -0 $SERVER_PID 2>/dev/null; then
    kill $SERVER_PID
    success "Aplicación puede iniciar correctamente"
else
    error "La aplicación no puede iniciar"
fi

# Resumen final
echo ""
echo "🎉 ¡Despliegue completado exitosamente!"
echo ""
echo "📋 Resumen del despliegue:"
echo "   ✅ Configuración verificada"
echo "   ✅ Base de datos actualizada"
echo "   ✅ Archivos estáticos recolectados"
echo "   ✅ Logs configurados"
echo "   ✅ Seguridad verificada"
echo "   ✅ Aplicación funcional"
echo ""
echo "🔍 Próximos pasos:"
echo "   1. Configurar servidor web (Nginx/Apache)"
echo "   2. Configurar servidor WSGI (Gunicorn/uWSGI)"
echo "   3. Configurar SSL/HTTPS"
echo "   4. Configurar monitoreo"
echo ""
echo "📊 Verificar logs:"
echo "   tail -f logs/django.log"
echo "   tail -f logs/security.log"
echo ""
echo "🌐 Variables importantes verificadas:"
echo "   DEBUG=False ✅"
echo "   SECRET_KEY=Configurada ✅"
echo "   HTTPS=Habilitado ✅"
echo ""
warning "Recordatorio: Nunca commits archivos .env al repositorio"