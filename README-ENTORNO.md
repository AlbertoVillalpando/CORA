# 🚀 Inicialización Automática del Entorno - CORA

## ⚡ Uso Rápido

### Linux/MacOS:
```bash
chmod +x init-env.sh
./init-env.sh
```

### Windows:
```cmd
init-env.bat
```

## 📋 ¿Qué hace el script?

El script automatiza completamente la configuración del entorno de desarrollo:

### ✅ **Verificaciones del Sistema**
- Verifica Python 3.8+ instalado
- Verifica pip instalado
- Confirma que estás en el directorio correcto del proyecto

### ✅ **Entorno Virtual**
- Crea automáticamente `venv/` si no existe
- Pregunta si quieres recrear el entorno si ya existe
- Activa el entorno virtual automáticamente

### ✅ **Dependencias**
- Actualiza pip a la última versión
- Instala todas las dependencias de `requirements.txt`
- Verifica que `django-environ` se instaló correctamente

### ✅ **Variables de Entorno**
- Copia `.env.example` a `.env` automáticamente
- **Genera SECRET_KEY segura única automáticamente**
- Configura todas las variables necesarias para desarrollo

### ✅ **Base de Datos**
- Verifica la configuración de Django
- Ejecuta todas las migraciones automáticamente
- Deja la BD lista para usar

### ✅ **Directorios**
- Crea `logs/` para archivos de log
- Crea `backups/` para respaldos
- Crea `media/conferencias_zips/` para archivos

### ✅ **Verificación Final**
- Verifica que Django funciona correctamente
- Confirma que SECRET_KEY está configurada
- Ejecuta `python manage.py check`

## 🎯 **Resultado**

Después de ejecutar el script:

```bash
# El entorno está listo, solo necesitas:
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

python manage.py runserver
```

## 🛠️ **Opciones Avanzadas** (Solo Linux/Mac)

```bash
# Ayuda
./init-env.sh --help

# Saltar creación de entorno virtual
./init-env.sh --skip-venv

# Saltar instalación de dependencias  
./init-env.sh --skip-deps

# Saltar configuración de base de datos
./init-env.sh --skip-db

# Modo verboso
./init-env.sh --verbose
```

## 🔧 **Problemas Comunes**

### Python no encontrado:
```bash
# Instalar Python 3.8+
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3                  # macOS
```

### Permisos en Linux:
```bash
chmod +x init-env.sh
```

### Error de venv en Ubuntu:
```bash
sudo apt install python3-venv
```

## 📊 **Comparación: Manual vs Automático**

| Tarea | Manual | Con Script |
|-------|--------|------------|
| Crear venv | `python3 -m venv venv` | ✅ Automático |
| Activar venv | `source venv/bin/activate` | ✅ Automático |
| Instalar deps | `pip install -r requirements.txt` | ✅ Automático |
| Configurar .env | Copiar y editar manualmente | ✅ Automático |
| Generar SECRET_KEY | Ejecutar comando de Django | ✅ Automático |
| Crear directorios | `mkdir logs backups media` | ✅ Automático |
| Migrar BD | `python manage.py migrate` | ✅ Automático |
| Verificar | `python manage.py check` | ✅ Automático |
| **TIEMPO TOTAL** | **~10-15 minutos** | **~2-3 minutos** |

## 🎉 **Ventajas del Script**

- ⚡ **Rapidez**: De 15 minutos a 3 minutos
- 🔒 **Seguridad**: SECRET_KEY única cada vez
- ✅ **Confiabilidad**: Verifica cada paso
- 🎨 **Visual**: Output colorido e informativo
- 🔄 **Reutilizable**: Puedes ejecutarlo múltiples veces
- 🛡️ **Detección de errores**: Para si algo falla
- 📱 **Multi-plataforma**: Linux, Mac y Windows
- 📋 **Completo**: Todo lo necesario para empezar

## 🔮 **Próximos Pasos Después del Script**

1. **Iniciar servidor**: `python manage.py runserver`
2. **Visitar**: http://localhost:8000
3. **Admin**: http://localhost:8000/admin
4. **Documentación completa**: `INSTALACION_SEGURA.md`

---

**💡 TIP**: Guarda este script para inicializar rápidamente el entorno en nuevas máquinas o después de clonar el repositorio.