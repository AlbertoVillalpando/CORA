@echo off
REM CORA Environment Initializer para Windows
REM Script para inicializar automáticamente el entorno virtual y configuración

setlocal EnableDelayedExpansion

REM Configuración de colores (si está disponible)
set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "CYAN=[36m"
set "NC=[0m"

REM Banner
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🏛️  CORA - Conference Review Management System           ║
echo ║     🔧  Environment Initializer (Windows)                   ║
echo ║     🎓  Universidad Autónoma de Zacatecas                    ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Función para mostrar información
:log_info
echo [INFO] %~1
goto :eof

:log_success
echo [SUCCESS] %~1
goto :eof

:log_warning
echo [WARNING] %~1
goto :eof

:log_error
echo [ERROR] %~1
exit /b 1

:log_step
echo.
echo [STEP] %~1
goto :eof

REM Verificar requisitos
call :log_step "Verificando requisitos del sistema..."

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        call :log_error "Python no está instalado o no está en el PATH"
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

%PYTHON_CMD% --version
call :log_success "Python encontrado"

REM Verificar pip
pip --version >nul 2>&1
if errorlevel 1 (
    call :log_error "pip no está instalado o no está en el PATH"
)
call :log_success "pip encontrado"

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    call :log_error "No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto CORA."
)
call :log_success "Directorio del proyecto verificado"

REM Crear entorno virtual
call :log_step "Configurando entorno virtual..."

if exist "venv" (
    call :log_warning "El entorno virtual ya existe en 'venv\'"
    set /p response="¿Deseas recrearlo? (y/N): "
    if /i "!response!"=="y" (
        call :log_info "Eliminando entorno virtual existente..."
        rmdir /s /q venv
    ) else (
        call :log_info "Usando entorno virtual existente"
        goto :activate_venv
    )
)

call :log_info "Creando nuevo entorno virtual..."
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    call :log_error "No se pudo crear el entorno virtual"
)
call :log_success "Entorno virtual creado en 'venv\'"

:activate_venv
REM Activar entorno virtual
call :log_step "Activando entorno virtual..."
call venv\Scripts\activate.bat
if errorlevel 1 (
    call :log_error "No se pudo activar el entorno virtual"
)
call :log_success "Entorno virtual activado"

REM Instalar dependencias
call :log_step "Instalando dependencias..."

call :log_info "Actualizando pip..."
python -m pip install --upgrade pip

call :log_info "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt
if errorlevel 1 (
    call :log_error "Error instalando dependencias"
)

call :log_info "Verificando instalación de django-environ..."
python -c "import environ; print('django-environ instalado correctamente')"
if errorlevel 1 (
    call :log_error "django-environ no se instaló correctamente"
)
call :log_success "Dependencias instaladas correctamente"

REM Configurar variables de entorno
call :log_step "Configurando variables de entorno..."

if not exist ".env" (
    if exist ".env.example" (
        call :log_info "Copiando configuración desde .env.example..."
        copy .env.example .env >nul
        
        call :log_info "Generando SECRET_KEY segura..."
        for /f "delims=" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set NEW_SECRET_KEY=%%i
        
        REM Reemplazar SECRET_KEY en .env usando PowerShell
        powershell -Command "(Get-Content .env) -replace 'your-secret-key-here', '%NEW_SECRET_KEY%' | Set-Content .env"
        
        call :log_success "Archivo .env configurado con SECRET_KEY segura"
    ) else (
        call :log_error "No se encontró .env.example. No se puede configurar el entorno."
    )
) else (
    call :log_warning "El archivo .env ya existe. No se modificará."
)

REM Crear directorios necesarios
call :log_step "Creando directorios necesarios..."

if not exist "logs" mkdir logs
if not exist "logs\django.log" echo. > logs\django.log
if not exist "logs\security.log" echo. > logs\security.log
if not exist "backups" mkdir backups
if not exist "media\conferencias_zips" mkdir media\conferencias_zips

call :log_success "Directorios creados correctamente"

REM Configurar base de datos
call :log_step "Configurando base de datos..."

call :log_info "Verificando configuración de Django..."
python manage.py check
if errorlevel 1 (
    call :log_error "La configuración de Django tiene errores"
)

call :log_info "Ejecutando migraciones de base de datos..."
python manage.py migrate
if errorlevel 1 (
    call :log_error "Error ejecutando migraciones"
)
call :log_success "Base de datos configurada correctamente"

REM Verificar instalación
call :log_step "Verificando instalación..."

python -c "import django; print(f'Django {django.get_version()} instalado')"
if errorlevel 1 (
    call :log_error "Django no funciona correctamente"
)

python manage.py check --verbosity=0
if errorlevel 1 (
    call :log_warning "Hay advertencias en la configuración"
)

call :log_success "Instalación verificada correctamente"

REM Información final
echo.
echo [SUCCESS] ¡Entorno inicializado exitosamente!
echo.
echo [INFO] Resumen de la configuración:
echo    ✅ Entorno virtual: venv\
echo    ✅ Dependencias instaladas correctamente
echo    ✅ Variables de entorno: .env
echo    ✅ Base de datos: db.sqlite3
echo    ✅ Logs: logs\
echo    ✅ Configuración verificada
echo.
echo [INFO] Para iniciar el servidor:
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo [INFO] Luego visita:
echo    🏠 Aplicación: http://localhost:8000
echo    👮 Admin: http://localhost:8000/admin
echo.
echo [INFO] Documentación:
echo    📖 Instalación completa: INSTALACION_SEGURA.md
echo    🔧 Configuración: CLAUDE.md
echo.
echo [INFO] Comandos útiles:
echo    🧪 Ejecutar tests: python manage.py test
echo    🔒 Verificar seguridad: python manage.py check --deploy
echo    📊 Ver logs: type logs\django.log
echo.
echo [INFO] Para reactivar el entorno en el futuro:
echo    venv\Scripts\activate
echo.
echo ✨ ¡Inicialización completada exitosamente! ✨

pause