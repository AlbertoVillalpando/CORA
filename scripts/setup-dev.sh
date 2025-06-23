#!/bin/bash

# Setup Development Environment - CORA
# Este script configura automáticamente el entorno de desarrollo seguro

echo "🚀 Configurando entorno de desarrollo CORA..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Verificar si estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    error "No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto."
fi

# Paso 1: Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    error "Python3 no está instalado. Por favor instala Python 3.8+"
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
success "Python $PYTHON_VERSION encontrado"

# Paso 2: Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv || error "No se pudo crear el entorno virtual"
    success "Entorno virtual creado"
else
    warning "Entorno virtual ya existe"
fi

# Paso 3: Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate || error "No se pudo activar el entorno virtual"
success "Entorno virtual activado"

# Paso 4: Actualizar pip
echo "📥 Actualizando pip..."
pip install --upgrade pip

# Paso 5: Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt || error "No se pudieron instalar las dependencias"
success "Dependencias instaladas correctamente"

# Paso 6: Verificar django-environ
echo "🔍 Verificando django-environ..."
python -c "import environ; print('django-environ importado correctamente')" || error "django-environ no se instaló correctamente"
success "django-environ verificado"

# Paso 7: Configurar variables de entorno
if [ ! -f ".env" ]; then
    echo "⚙️  Configurando variables de entorno..."
    cp .env.example .env || error "No se pudo copiar .env.example"
    
    # Generar nueva SECRET_KEY
    echo "🔐 Generando SECRET_KEY segura..."
    NEW_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    
    # Reemplazar en .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here/$NEW_SECRET_KEY/g" .env
    else
        # Linux
        sed -i "s/your-secret-key-here/$NEW_SECRET_KEY/g" .env
    fi
    
    success "Archivo .env configurado con SECRET_KEY segura"
else
    warning "Archivo .env ya existe"
fi

# Paso 8: Crear directorio de logs
echo "📁 Creando directorio de logs..."
mkdir -p logs
touch logs/django.log
touch logs/security.log
success "Directorio de logs creado"

# Paso 9: Ejecutar verificaciones de Django
echo "🔍 Verificando configuración de Django..."
python manage.py check || error "La configuración de Django tiene errores"
success "Configuración de Django verificada"

# Paso 10: Ejecutar migraciones
echo "💾 Ejecutando migraciones..."
python manage.py migrate || error "Las migraciones fallaron"
success "Migraciones ejecutadas correctamente"

# Paso 11: Verificar configuración de seguridad
echo "🔒 Verificando configuración de seguridad..."
python manage.py check --deploy --verbosity=0 || warning "Hay advertencias de seguridad (normal en desarrollo)"

# Paso 12: Crear superusuario si no existe
echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No hay superusuarios. Creando uno...')
    User.objects.create_superuser('admin', 'admin@cora.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
"

# Resumen final
echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo ""
echo "📋 Resumen:"
echo "   ✅ Entorno virtual: venv/"
echo "   ✅ Dependencias instaladas"
echo "   ✅ Variables de entorno: .env"
echo "   ✅ Base de datos: db.sqlite3"
echo "   ✅ Logs: logs/"
echo "   ✅ Superusuario: admin/admin123"
echo ""
echo "🚀 Para iniciar el servidor:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 Luego visita: http://localhost:8000"
echo "👮 Admin: http://localhost:8000/admin"
echo ""
echo "📚 Documentación completa: INSTALACION_SEGURA.md"