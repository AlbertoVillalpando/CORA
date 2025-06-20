# GUÍA DE REDISEÑO FRONTEND - PROYECTO CORA

## 📋 RESUMEN EJECUTIVO

Este documento establece el plan de trabajo para mejorar el frontend del sistema CORA (Conference Review Application), enfocándose en:
- Mejor estructura de código UI
- Rediseño representativo del propósito académico
- Mejora significativa de UI/UX

## 🎯 OBJETIVOS PRINCIPALES

1. **Estandarización Visual**: Crear un sistema de diseño consistente y profesional
2. **Identidad Académica**: Reflejar el propósito universitario y académico de la plataforma
3. **Experiencia de Usuario**: Mejorar la usabilidad y navegación
4. **Código Mantenible**: Estructurar el código frontend de manera escalable
5. **Responsividad**: Garantizar funcionamiento óptimo en todos los dispositivos

## 📊 VISTAS IDENTIFICADAS PARA MODIFICAR

### **🔴 PRIORIDAD CRÍTICA (Base del Sistema)**
1. **`home/templates/base.html`** - Template base principal
2. **`home/templates/home.html`** - Página de inicio/landing
3. **`usuarios/templates/usuarios/login.html`** - Página de autenticación
4. **`usuarios/templates/usuarios/registro.html`** - Registro de usuarios

### **🟡 PRIORIDAD ALTA (Paneles Principales)**
5. **`usuarios/templates/usuarios/vistaAdmin.html`** - Dashboard administrativo
6. **`usuarios/templates/usuarios/vistaAutor.html`** - Panel del autor
7. **`usuarios/templates/usuarios/vistaOrganizador.html`** - Panel del organizador
8. **`usuarios/templates/usuarios/vistaRevisor.html`** - Panel del revisor
9. **`usuarios/templates/usuarios/home.html`** - Home personalizado por rol

### **🟢 PRIORIDAD MEDIA (Funcionalidades Core)**
10. **`conferencia/templates/conferencia/crear_conferencia.html`** - Creación de conferencias
11. **`conferencia/templates/conferencia/conferencias_administrador.html`** - Gestión admin
12. **`conferencia/templates/conferencia/conferencias_autor.html`** - Vista autor
13. **`conferencia/templates/conferencia/conferencias_organizador.html`** - Vista organizador
14. **`conferencia/templates/conferencia/conferencias_revisor.html`** - Vista revisor
15. **`conferencia/templates/conferencia/invitaciones_conferencia.html`** - Gestión de invitaciones
16. **`conferencia/templates/conferencia/subir_documentos.html`** - Subida de archivos

### **🔵 PRIORIDAD BAJA (Funcionalidades Específicas)**
17. **`formulario/templates/formulario/crear_formulario.html`** - Creación de formularios
18. **`formulario/templates/formulario/evaluar_conferencia.html`** - Evaluación
19. **`formulario/templates/formulario/ver_evaluacion.html`** - Visualización de evaluaciones
20. **`formulario/templates/formulario/ver_formulario.html`** - Visualización de formularios
21. **`usuarios/templates/usuarios/admin_dashboard.html`** - Dashboard específico admin
22. **`usuarios/templates/usuarios/invitaciones.html`** - Gestión de invitaciones usuario
23. **`notificaciones/templates/notificaciones/_dropdown.html`** - Sistema de notificaciones

### **⚪ TEMPLATES DE SOPORTE**
24. **`registration/password_reset_*.html`** (4 archivos) - Restablecimiento de contraseña
25. **`usuarios/templates/usuarios/vistaAdmin.html`** - Vista adicional admin

**TOTAL: 25+ vistas a modificar**

## 🏗️ NUEVA ESTRUCTURA DE CARPETAS PROPUESTA

```
easy-chair-uaz/
├── static/
│   ├── assets/
│   │   ├── css/
│   │   │   ├── core/
│   │   │   │   ├── base.css                    # Estilos base y reset
│   │   │   │   ├── variables.css               # Variables CSS (colores UAZ, tipografía)
│   │   │   │   ├── typography.css              # Sistema tipográfico
│   │   │   │   └── layout.css                  # Layouts y grids
│   │   │   ├── components/
│   │   │   │   ├── buttons.css                 # Sistema de botones
│   │   │   │   ├── forms.css                   # Formularios estandarizados
│   │   │   │   ├── tables.css                  # Tablas académicas
│   │   │   │   ├── cards.css                   # Cards y contenedores
│   │   │   │   ├── navigation.css              # Navegación y menús
│   │   │   │   ├── notifications.css           # Sistema de notificaciones
│   │   │   │   └── modals.css                  # Modales y overlays
│   │   │   ├── pages/
│   │   │   │   ├── auth.css                    # Páginas de autenticación
│   │   │   │   ├── dashboard.css               # Dashboards por rol
│   │   │   │   ├── conferences.css             # Gestión de conferencias
│   │   │   │   ├── evaluations.css             # Sistema de evaluación
│   │   │   │   └── admin.css                   # Páginas administrativas
│   │   │   ├── themes/
│   │   │   │   ├── uaz-academic.css            # Tema académico UAZ
│   │   │   │   └── uaz-brand.css               # Branding institucional
│   │   │   └── utilities/
│   │   │       ├── responsive.css              # Utilidades responsive
│   │   │       ├── animations.css              # Animaciones académicas
│   │   │       └── accessibility.css           # Mejoras de accesibilidad
│   │   ├── js/
│   │   │   ├── core/
│   │   │   │   ├── app.js                      # JavaScript principal
│   │   │   │   ├── utils.js                    # Utilidades generales
│   │   │   │   └── api.js                      # Comunicación con backend
│   │   │   ├── components/
│   │   │   │   ├── forms.js                    # Validación de formularios
│   │   │   │   ├── tables.js                   # Funcionalidad de tablas
│   │   │   │   ├── notifications.js            # Sistema de notificaciones
│   │   │   │   ├── file-upload.js              # Subida de archivos
│   │   │   │   └── modals.js                   # Gestión de modales
│   │   │   ├── pages/
│   │   │   │   ├── dashboard.js                # Funcionalidad dashboards
│   │   │   │   ├── conferences.js              # Gestión conferencias
│   │   │   │   ├── evaluations.js              # Sistema evaluación
│   │   │   │   └── admin.js                    # Funciones administrativas
│   │   │   └── vendors/
│   │   │       ├── chart.min.js                # Gráficos para métricas
│   │   │       ├── datepicker.min.js           # Selector de fechas
│   │   │       └── sortable.min.js             # Tablas ordenables
│   │   ├── img/
│   │   │   ├── branding/
│   │   │   │   ├── uaz-logo.svg                # Logo UAZ optimizado
│   │   │   │   ├── uaz-logo-white.svg          # Logo blanco
│   │   │   │   ├── cora-logo.svg               # Logo del sistema
│   │   │   │   └── favicon/                    # Favicons
│   │   │   ├── icons/
│   │   │   │   ├── academic/                   # Iconos académicos
│   │   │   │   ├── actions/                    # Iconos de acciones
│   │   │   │   └── status/                     # Iconos de estado
│   │   │   ├── illustrations/
│   │   │   │   ├── conference-hero.svg         # Ilustración principal
│   │   │   │   ├── empty-states/               # Estados vacíos
│   │   │   │   └── onboarding/                 # Ilustraciones de guía
│   │   │   └── backgrounds/
│   │   │       ├── academic-pattern.svg        # Patrones académicos
│   │   │       └── uaz-gradient.jpg            # Gradiente institucional
│   │   └── fonts/
│   │       ├── academic/                       # Tipografía académica
│   │       └── icons/                          # Fuentes de iconos
│   └── build/                                  # Archivos compilados/minificados
├── templates/
│   ├── base/
│   │   ├── base.html                          # Template base principal
│   │   ├── base_auth.html                     # Base para autenticación
│   │   ├── base_dashboard.html                # Base para dashboards
│   │   └── base_public.html                   # Base para páginas públicas
│   ├── components/
│   │   ├── navigation/
│   │   │   ├── navbar.html                    # Barra de navegación principal
│   │   │   ├── sidebar.html                   # Menú lateral
│   │   │   ├── breadcrumbs.html               # Migas de pan
│   │   │   └── user-menu.html                 # Menú de usuario
│   │   ├── forms/
│   │   │   ├── form-field.html                # Campo de formulario genérico
│   │   │   ├── form-actions.html              # Botones de acción
│   │   │   ├── form-validation.html           # Mensajes de validación
│   │   │   └── file-upload.html               # Componente subida archivos
│   │   ├── tables/
│   │   │   ├── data-table.html                # Tabla de datos genérica
│   │   │   ├── table-actions.html             # Acciones de tabla
│   │   │   ├── table-filters.html             # Filtros de tabla
│   │   │   └── pagination.html                # Paginación
│   │   ├── cards/
│   │   │   ├── conference-card.html           # Card de conferencia
│   │   │   ├── metric-card.html               # Card de métrica
│   │   │   ├── user-card.html                 # Card de usuario
│   │   │   └── notification-card.html         # Card de notificación
│   │   ├── modals/
│   │   │   ├── confirmation-modal.html        # Modal de confirmación
│   │   │   ├── info-modal.html                # Modal informativo
│   │   │   └── form-modal.html                # Modal con formulario
│   │   └── alerts/
│   │       ├── success-alert.html             # Alerta de éxito
│   │       ├── error-alert.html               # Alerta de error
│   │       ├── warning-alert.html             # Alerta de advertencia
│   │       └── info-alert.html                # Alerta informativa
│   └── pages/
│       ├── errors/
│       │   ├── 404.html                       # Página 404 académica
│       │   ├── 403.html                       # Página 403 académica
│       │   └── 500.html                       # Página 500 académica
│       └── maintenance/
│           └── maintenance.html               # Página de mantenimiento
├── (apps existentes con templates modificados)
│   ├── home/templates/home/
│   ├── usuarios/templates/usuarios/
│   ├── conferencia/templates/conferencia/
│   ├── formulario/templates/formulario/
│   └── notificaciones/templates/notificaciones/
└── frontend_docs/                             # Documentación del frontend
    ├── design-system.md                       # Sistema de diseño
    ├── component-library.md                   # Librería de componentes
    ├── style-guide.md                         # Guía de estilos
    └── development-guide.md                   # Guía de desarrollo frontend
```

## 🎨 SISTEMA DE DISEÑO PROPUESTO

### **Paleta de Colores UAZ Académica**
```css
:root {
  /* Colores Primarios UAZ */
  --uaz-red: #8B0000;              /* Rojo institucional */
  --uaz-gold: #FFD700;             /* Oro institucional */
  --uaz-dark: #2C1810;             /* Marrón oscuro */
  
  /* Colores Académicos */
  --academic-blue: #1E3A8A;        /* Azul académico */
  --academic-gray: #64748B;        /* Gris profesional */
  --academic-green: #059669;       /* Verde éxito */
  
  /* Colores de Estado */
  --status-pending: #F59E0B;       /* Amarillo pendiente */
  --status-approved: #10B981;      /* Verde aprobado */
  --status-rejected: #EF4444;      /* Rojo rechazado */
  --status-draft: #6B7280;         /* Gris borrador */
  
  /* Neutrales */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-500: #6B7280;
  --gray-700: #374151;
  --gray-900: #111827;
}
```

### **Tipografía Académica**
```css
:root {
  /* Fuentes principales */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Merriweather', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Escalas tipográficas */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
}
```

## 📋 PLAN DE TRABAJO DETALLADO

### **FASE 1: FUNDACIÓN DEL SISTEMA (Semana 1-2)**

#### **1.1 Configuración Base**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/core/
├── base.css                    # Reset CSS + estilos base
├── variables.css               # Variables CSS del sistema
├── typography.css              # Sistema tipográfico
└── layout.css                  # Grids y layouts

static/assets/css/themes/
├── uaz-academic.css            # Tema académico UAZ
└── uaz-brand.css               # Branding institucional

static/assets/img/branding/
├── uaz-logo.svg                # Logo UAZ optimizado
├── uaz-logo-white.svg          # Logo blanco
├── cora-logo.svg               # Logo del sistema
└── favicon/
    ├── favicon.ico
    ├── favicon-16x16.png
    ├── favicon-32x32.png
    └── apple-touch-icon.png

frontend_docs/
├── design-system.md            # Sistema de diseño
└── style-guide.md              # Guía de estilos
```

**✅ TAREAS:**
- [ ] Crear estructura de carpetas `/static/assets/`
- [ ] Configurar variables CSS en `core/variables.css`
- [ ] Implementar sistema tipográfico en `core/typography.css`
- [ ] Establecer layouts base en `core/layout.css`
- [ ] Crear tema académico UAZ en `themes/uaz-academic.css`
- [ ] Optimizar logos y crear favicons
- [ ] Documentar sistema de diseño

#### **1.2 Templates Base**

**🆕 ARCHIVOS A CREAR:**
```
templates/base/
├── base.html                   # Template base principal
├── base_auth.html              # Base para autenticación
├── base_dashboard.html         # Base para dashboards
└── base_public.html            # Base para páginas públicas

templates/components/navigation/
├── navbar.html                 # Barra de navegación principal
├── sidebar.html                # Menú lateral
├── breadcrumbs.html            # Migas de pan
└── user-menu.html              # Menú de usuario
```

**🔄 ARCHIVOS A MODIFICAR:**
```
home/templates/base.html        # Refactorizar template base actual
```

**✅ TAREAS:**
- [ ] Rediseñar `base.html` con nueva estructura
- [ ] Crear `base_auth.html` para páginas de autenticación
- [ ] Crear `base_dashboard.html` para dashboards
- [ ] Crear `base_public.html` para páginas públicas
- [ ] Implementar componente de navegación en `navbar.html`
- [ ] Crear menú lateral responsivo en `sidebar.html`
- [ ] Implementar breadcrumbs en `breadcrumbs.html`
- [ ] Crear dropdown de usuario en `user-menu.html`

#### **1.3 Componentes Core**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/components/
├── buttons.css                 # Sistema de botones
├── forms.css                   # Formularios estandarizados
├── tables.css                  # Tablas académicas
├── cards.css                   # Cards y contenedores
├── navigation.css              # Navegación y menús
├── notifications.css           # Sistema de notificaciones
└── modals.css                  # Modales y overlays

templates/components/forms/
├── form-field.html             # Campo de formulario genérico
├── form-actions.html           # Botones de acción
├── form-validation.html        # Mensajes de validación
└── file-upload.html            # Componente subida archivos

templates/components/tables/
├── data-table.html             # Tabla de datos genérica
├── table-actions.html          # Acciones de tabla
├── table-filters.html          # Filtros de tabla
└── pagination.html             # Paginación

templates/components/cards/
├── conference-card.html        # Card de conferencia
├── metric-card.html            # Card de métrica
├── user-card.html              # Card de usuario
└── notification-card.html      # Card de notificación

templates/components/alerts/
├── success-alert.html          # Alerta de éxito
├── error-alert.html            # Alerta de error
├── warning-alert.html          # Alerta de advertencia
└── info-alert.html             # Alerta informativa

static/assets/js/components/
├── forms.js                    # Validación de formularios
├── tables.js                   # Funcionalidad de tablas
├── notifications.js            # Sistema de notificaciones
└── modals.js                   # Gestión de modales
```

**✅ TAREAS:**
- [ ] Desarrollar sistema de botones estandarizado
- [ ] Crear componentes de formulario reutilizables
- [ ] Implementar sistema de cards académicos
- [ ] Diseñar componentes de tabla responsivos
- [ ] Crear sistema de alertas consistente
- [ ] Implementar modales reutilizables
- [ ] Desarrollar JavaScript para componentes interactivos

### **FASE 2: REDISEÑO DE AUTENTICACIÓN (Semana 2-3)**

#### **2.1 Páginas de Auth**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/pages/
└── auth.css                    # Estilos páginas autenticación

static/assets/img/illustrations/
├── conference-hero.svg         # Ilustración principal
├── auth-background.svg         # Background para auth
└── onboarding/
    ├── welcome-organizer.svg   # Bienvenida organizador
    ├── welcome-author.svg      # Bienvenida autor
    ├── welcome-reviewer.svg    # Bienvenida revisor
    └── welcome-admin.svg       # Bienvenida admin

static/assets/js/pages/
└── auth.js                     # JavaScript para autenticación

templates/components/auth/
├── login-form.html             # Formulario de login
├── register-form.html          # Formulario de registro
├── password-reset-form.html    # Formulario reset password
└── onboarding-steps.html       # Pasos de onboarding
```

**🔄 ARCHIVOS A MODIFICAR:**
```
usuarios/templates/usuarios/
├── login.html                  # Página de login
├── registro.html               # Página de registro
└── home.html                   # Home con onboarding

usuarios/templates/registration/
├── password_reset_form.html    # Formulario reset
├── password_reset_done.html    # Confirmación envío
├── password_reset_confirm.html # Confirmación reset
└── password_reset_complete.html # Reset completado
```

**✅ TAREAS:**
- [ ] Crear estilos CSS específicos para auth en `auth.css`
- [ ] Rediseñar `login.html` con identidad UAZ y nueva estructura
- [ ] Mejorar `registro.html` con validación visual paso a paso
- [ ] Actualizar 4 templates de recuperación de contraseña
- [ ] Crear componentes reutilizables de formularios auth
- [ ] Diseñar ilustraciones académicas apropiadas
- [ ] Implementar onboarding visual para nuevos usuarios
- [ ] Crear JavaScript para validación de formularios

#### **2.2 Mejoras UX Auth**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/js/core/
├── validation.js               # Validación en tiempo real
└── feedback.js                 # Sistema de feedback visual

templates/components/feedback/
├── validation-tooltip.html     # Tooltips de validación
├── success-message.html        # Mensajes de éxito
└── error-message.html          # Mensajes de error
```

**✅ TAREAS:**
- [ ] Implementar validación en tiempo real con `validation.js`
- [ ] Crear sistema de feedback visual con tooltips
- [ ] Añadir ilustraciones académicas en formularios
- [ ] Optimizar formularios para dispositivos móviles
- [ ] Implementar indicadores de fuerza de contraseña
- [ ] Crear animaciones sutiles para transiciones
- [ ] Agregar estados de carga en botones de envío

### **FASE 3: DASHBOARDS PRINCIPALES (Semana 3-5)**

#### **3.1 Dashboard Base**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/pages/
└── dashboard.css               # Estilos para dashboards

static/assets/js/pages/
├── dashboard.js                # Funcionalidad dashboards
└── metrics.js                  # Gráficos y métricas

static/assets/js/vendors/
├── chart.min.js                # Gráficos para métricas
├── datepicker.min.js           # Selector de fechas
└── sortable.min.js             # Tablas ordenables

templates/components/dashboard/
├── stats-widget.html           # Widget de estadísticas
├── chart-widget.html           # Widget de gráfico
├── recent-activity.html        # Actividad reciente
├── quick-actions.html          # Acciones rápidas
└── progress-indicator.html     # Indicadores de progreso

templates/components/navigation/
├── role-sidebar.html           # Sidebar específico por rol
└── dashboard-tabs.html         # Pestañas de dashboard
```

**🔄 ARCHIVOS A MODIFICAR:**
```
home/templates/home.html        # Página principal/landing
usuarios/templates/usuarios/home.html # Home por rol
```

**✅ TAREAS:**
- [ ] Crear estructura CSS base para dashboards en `dashboard.css`
- [ ] Implementar widgets de métricas reutilizables
- [ ] Crear gráficos interactivos con Chart.js
- [ ] Diseñar navegación contextual por rol
- [ ] Implementar sistema de accesos rápidos
- [ ] Crear indicadores de progreso y KPIs
- [ ] Integrar librerías de terceros (charts, datepicker)

#### **3.2 Dashboards Específicos**

**🆕 ARCHIVOS A CREAR:**
```
templates/components/dashboard/admin/
├── system-metrics.html         # Métricas del sistema
├── user-management.html        # Gestión de usuarios
├── conference-overview.html    # Resumen conferencias
└── reports-section.html        # Sección de reportes

templates/components/dashboard/organizer/
├── my-conferences.html         # Mis conferencias
├── reviewer-management.html    # Gestión revisores
├── submissions-status.html     # Estado de envíos
└── deadlines-calendar.html     # Calendario fechas límite

templates/components/dashboard/author/
├── my-submissions.html         # Mis envíos
├── review-status.html          # Estado de revisiones
├── feedback-summary.html       # Resumen feedback
└── upcoming-deadlines.html     # Fechas límite próximas

templates/components/dashboard/reviewer/
├── review-queue.html           # Cola de revisiones
├── assigned-papers.html        # Trabajos asignados
├── review-progress.html        # Progreso de revisiones
└── evaluation-forms.html       # Formularios de evaluación
```

**🔄 ARCHIVOS A MODIFICAR:**
```
usuarios/templates/usuarios/
├── vistaAdmin.html             # Dashboard administrativo
├── vistaOrganizador.html       # Dashboard organizador
├── vistaAutor.html             # Dashboard autor
├── vistaRevisor.html           # Dashboard revisor
└── admin_dashboard.html        # Dashboard admin específico
```

**✅ TAREAS:**
- [ ] **Vista Admin**: Rediseñar con métricas del sistema, gestión usuarios
- [ ] **Vista Organizador**: Panel de conferencias, gestión revisores, calendario
- [ ] **Vista Autor**: Seguimiento envíos, estado revisiones, feedback
- [ ] **Vista Revisor**: Cola de trabajos, herramientas evaluación, progreso
- [ ] Implementar navegación específica por rol
- [ ] Crear widgets personalizados para cada dashboard
- [ ] Integrar notificaciones contextuales por rol
- [ ] Optimizar layouts para diferentes resoluciones

### **FASE 4: GESTIÓN DE CONFERENCIAS (Semana 5-7)**

#### **4.1 CRUD Conferencias**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/pages/
└── conferences.css             # Estilos gestión conferencias

static/assets/js/pages/
└── conferences.js              # Funcionalidad conferencias

templates/components/conferences/
├── conference-wizard.html      # Wizard creación por steps
├── conference-card-detailed.html # Card detallada conferencia
├── conference-filters.html     # Filtros avanzados
├── conference-actions.html     # Acciones conferencia
└── conference-timeline.html    # Timeline del proceso

templates/components/forms/
├── conference-form-step1.html  # Paso 1: Info básica
├── conference-form-step2.html  # Paso 2: Detalles académicos
├── conference-form-step3.html  # Paso 3: Fechas y plazos
└── conference-form-step4.html  # Paso 4: Revisión final
```

**🔄 ARCHIVOS A MODIFICAR:**
```
conferencia/templates/conferencia/
├── crear_conferencia.html      # Creación con wizard
├── conferencias_administrador.html # Vista admin conferencias
├── conferencias_organizador.html # Vista organizador
├── conferencias_autor.html     # Vista autor
├── conferencias_revisor.html   # Vista revisor
├── editar.html                 # Edición de conferencia
└── invitaciones_conferencia.html # Gestión invitaciones
```

**✅ TAREAS:**
- [ ] Crear wizard de creación paso a paso con validación
- [ ] Rediseñar vistas de listado con filtros avanzados
- [ ] Implementar búsqueda en tiempo real
- [ ] Crear vista detalle enriquecida con timeline
- [ ] Optimizar flujo de edición con formularios modulares
- [ ] Implementar acciones masivas para administradores
- [ ] Crear sistema de estados visuales (borrador, activo, cerrado)
- [ ] Añadir indicadores de progreso de revisión

#### **4.2 Gestión de Archivos**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/components/
└── file-upload.css             # Estilos subida archivos

static/assets/js/components/
└── file-upload.js              # Funcionalidad drag & drop

templates/components/files/
├── drag-drop-zone.html         # Zona drag & drop
├── file-preview.html           # Preview de archivos
├── upload-progress.html        # Progreso de subida
├── file-validation.html        # Validación archivos
└── zip-contents-viewer.html    # Visor contenido ZIP

static/assets/img/icons/
├── file-types/                 # Iconos tipos archivo
│   ├── zip-icon.svg
│   ├── pdf-icon.svg
│   ├── doc-icon.svg
│   └── image-icon.svg
└── upload/
    ├── drag-drop-icon.svg
    └── upload-progress.svg
```

**🔄 ARCHIVOS A MODIFICAR:**
```
conferencia/templates/conferencia/
└── subir_documentos.html       # Interfaz subida mejorada
```

**✅ TAREAS:**
- [ ] Rediseñar interfaz con drag & drop moderno
- [ ] Implementar preview de archivos ZIP con listado contenido
- [ ] Añadir validación visual (tamaño, tipo, estructura)
- [ ] Crear barra de progreso animada para subidas
- [ ] Implementar detección automática de tipo de archivo
- [ ] Añadir compresión y optimización automática
- [ ] Crear sistema de versionado de archivos
- [ ] Implementar validación de integridad de archivos ZIP

### **FASE 5: SISTEMA DE EVALUACIÓN (Semana 7-8)**

#### **5.1 Formularios Dinámicos**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/pages/
└── evaluations.css             # Estilos sistema evaluación

static/assets/js/pages/
└── evaluations.js              # Funcionalidad evaluaciones

templates/components/evaluations/
├── form-builder.html           # Constructor de formularios
├── question-types.html         # Tipos de preguntas
├── drag-drop-questions.html    # Preguntas drag & drop
├── evaluation-interface.html   # Interfaz de evaluación
├── scoring-system.html         # Sistema de puntuación
└── evaluation-progress.html    # Progreso evaluación

templates/components/forms/dynamic/
├── rating-scale.html           # Escala de calificación
├── text-area-question.html     # Pregunta texto libre
├── multiple-choice.html        # Pregunta opción múltiple
├── likert-scale.html           # Escala Likert
└── file-upload-question.html   # Pregunta con archivo

static/assets/js/components/
├── form-builder.js             # Constructor drag & drop
└── evaluation-engine.js        # Motor de evaluación
```

**🔄 ARCHIVOS A MODIFICAR:**
```
formulario/templates/formulario/
├── crear_formulario.html       # Creador con drag & drop
├── evaluar_conferencia.html    # Interfaz evaluación mejorada
├── ver_evaluacion.html         # Visualización resultados
└── ver_formulario.html         # Vista previa formulario
```

**✅ TAREAS:**
- [ ] Crear constructor de formularios con drag & drop
- [ ] Implementar diferentes tipos de preguntas académicas
- [ ] Rediseñar interfaz de evaluación con mejor UX
- [ ] Optimizar formularios para dispositivos móviles
- [ ] Crear sistema de guardado automático de evaluaciones
- [ ] Implementar validación dinámica de respuestas
- [ ] Añadir indicadores de progreso en evaluaciones
- [ ] Crear templates reutilizables para tipos de pregunta

#### **5.2 Reportes y Analytics**

**🆕 ARCHIVOS A CREAR:**
```
templates/components/reports/
├── evaluation-dashboard.html   # Dashboard de evaluaciones
├── metrics-overview.html       # Resumen de métricas
├── scoring-charts.html         # Gráficos de puntuación
├── feedback-summary.html       # Resumen feedback
└── comparison-reports.html     # Reportes comparativos

templates/components/exports/
├── pdf-report-template.html    # Template PDF académico
├── excel-export-config.html    # Configuración export Excel
└── print-friendly-report.html  # Reporte para impresión

static/assets/js/components/
├── charts-evaluation.js        # Gráficos evaluación
├── export-manager.js           # Gestión exportaciones
└── report-generator.js         # Generador reportes

static/assets/css/components/
├── charts.css                  # Estilos gráficos
└── reports.css                 # Estilos reportes
```

**✅ TAREAS:**
- [ ] Crear dashboard de métricas de evaluación con gráficos
- [ ] Implementar exportación mejorada (PDF académico profesional)
- [ ] Añadir visualizaciones de datos interactivas
- [ ] Crear reportes automáticos programables
- [ ] Implementar comparación entre evaluaciones
- [ ] Añadir filtros avanzados para reportes
- [ ] Crear templates de reportes personalizables
- [ ] Implementar sistema de alertas por métricas

### **FASE 6: OPTIMIZACIÓN Y PULIDO (Semana 8-9)**

#### **6.1 Performance y Responsividad**

**🆕 ARCHIVOS A CREAR:**
```
static/assets/css/utilities/
├── responsive.css              # Utilidades responsive
├── animations.css              # Animaciones académicas
└── accessibility.css           # Mejoras de accesibilidad

static/build/
├── css/
│   ├── critical.min.css        # CSS crítico minificado
│   ├── main.min.css            # CSS principal minificado
│   └── vendor.min.css          # CSS de terceros minificado
├── js/
│   ├── critical.min.js         # JS crítico minificado
│   ├── main.min.js             # JS principal minificado
│   └── vendor.min.js           # JS de terceros minificado
└── img/
    └── optimized/              # Imágenes optimizadas

build-tools/
├── gulpfile.js                 # Automatización con Gulp
├── webpack.config.js           # Configuración Webpack
├── postcss.config.js           # Configuración PostCSS
└── optimization/
    ├── css-optimizer.js        # Optimizador CSS
    ├── js-optimizer.js         # Optimizador JS
    └── image-optimizer.js      # Optimizador imágenes

templates/components/performance/
├── lazy-loading.html           # Componente lazy loading
├── critical-css.html           # CSS crítico inline
└── preload-resources.html      # Preload de recursos
```

**🔄 ARCHIVOS A MODIFICAR:**
```
(Todos los templates existentes para optimización)
- Optimización de imágenes
- Minificación de assets
- Lazy loading implementation
- Critical CSS inlining
```

**✅ TAREAS:**
- [ ] Configurar sistema de build con Gulp/Webpack
- [ ] Optimizar CSS (minificación, purge de código no usado)
- [ ] Implementar lazy loading para imágenes y componentes
- [ ] Crear sistema de CSS crítico inline
- [ ] Optimizar JavaScript (minificación, code splitting)
- [ ] Comprimir y optimizar imágenes automáticamente
- [ ] Testear en todos los dispositivos y navegadores
- [ ] Implementar preload de recursos críticos
- [ ] Configurar CDN para assets estáticos

#### **6.2 Accesibilidad y SEO**

**🆕 ARCHIVOS A CREAR:**
```
templates/components/accessibility/
├── screen-reader-content.html  # Contenido para lectores pantalla
├── keyboard-navigation.html    # Navegación por teclado
├── focus-indicators.html       # Indicadores de foco
└── aria-labels.html            # Labels ARIA

static/assets/css/utilities/
└── accessibility.css           # Estilos accesibilidad

accessibility-config/
├── axe-config.json             # Configuración axe-core
├── lighthouse-config.json      # Configuración Lighthouse
└── wcag-checklist.md           # Checklist WCAG 2.1

seo-optimization/
├── meta-tags.html              # Meta tags optimizados
├── structured-data.json        # Datos estructurados
├── sitemap-generator.py        # Generador sitemap
└── robots-txt-template.txt     # Template robots.txt
```

**🔄 ARCHIVOS A MODIFICAR:**
```
(Todos los templates para mejoras de accesibilidad)
- Añadir ARIA labels y roles
- Mejorar navegación por teclado
- Optimizar para lectores de pantalla
- Implementar skip links
- Mejorar contraste de colores
- Añadir meta tags SEO
```

**✅ TAREAS:**
- [ ] Implementar estándares WCAG 2.1 AA
- [ ] Añadir ARIA labels, roles y properties
- [ ] Optimizar navegación por teclado con tab order
- [ ] Implementar skip links para navegación rápida
- [ ] Mejorar indicadores de foco visual
- [ ] Optimizar contraste de colores (mínimo 4.5:1)
- [ ] Añadir texto alternativo para todas las imágenes
- [ ] Implementar heading hierarchy correcta (h1-h6)
- [ ] Crear contenido alternativo para lectores de pantalla
- [ ] Optimizar meta tags y structured data para SEO

### **FASE 7: TESTING Y DOCUMENTACIÓN (Semana 9-10)**

#### **7.1 Testing Frontend**

**🆕 ARCHIVOS A CREAR:**
```
frontend-tests/
├── unit/
│   ├── components/
│   │   ├── buttons.test.js     # Tests sistema botones
│   │   ├── forms.test.js       # Tests componentes formulario
│   │   ├── tables.test.js      # Tests componentes tabla
│   │   └── cards.test.js       # Tests componentes cards
│   ├── pages/
│   │   ├── auth.test.js        # Tests páginas auth
│   │   ├── dashboard.test.js   # Tests dashboards
│   │   └── conferences.test.js # Tests gestión conferencias
│   └── utils/
│       ├── validation.test.js  # Tests validación
│       └── helpers.test.js     # Tests helpers
├── integration/
│   ├── user-flows/
│   │   ├── login-flow.test.js  # Flujo completo login
│   │   ├── conference-creation.test.js # Creación conferencia
│   │   └── evaluation-process.test.js  # Proceso evaluación
│   └── api-integration/
│       ├── auth-api.test.js    # Integración API auth
│       └── conference-api.test.js # Integración API conferencias
├── visual/
│   ├── screenshots/
│   │   ├── baseline/           # Screenshots base
│   │   └── current/            # Screenshots actuales
│   ├── visual-regression/
│   │   ├── login-page.test.js  # Regresión visual login
│   │   ├── dashboard.test.js   # Regresión visual dashboard
│   │   └── forms.test.js       # Regresión visual formularios
│   └── responsive/
│       ├── mobile.test.js      # Tests responsive móvil
│       ├── tablet.test.js      # Tests responsive tablet
│       └── desktop.test.js     # Tests responsive desktop
├── accessibility/
│   ├── axe-tests/
│   │   ├── pages.test.js       # Tests accesibilidad páginas
│   │   └── components.test.js  # Tests accesibilidad componentes
│   ├── keyboard-navigation/
│   │   ├── tab-order.test.js   # Tests orden tabulación
│   │   └── shortcuts.test.js   # Tests atajos teclado
│   └── screen-reader/
│       ├── aria-labels.test.js # Tests ARIA labels
│       └── semantic.test.js    # Tests semántica HTML
├── performance/
│   ├── lighthouse/
│   │   ├── performance.test.js # Tests performance
│   │   ├── seo.test.js         # Tests SEO
│   │   └── best-practices.test.js # Tests mejores prácticas
│   ├── load-testing/
│   │   ├── page-load.test.js   # Tests carga páginas
│   │   └── asset-load.test.js  # Tests carga assets
│   └── bundle-analysis/
│       ├── css-analysis.test.js # Análisis CSS
│       └── js-analysis.test.js  # Análisis JavaScript
└── usability/
    ├── task-completion/
    │   ├── conference-tasks.test.js # Tareas conferencias
    │   └── evaluation-tasks.test.js # Tareas evaluación
    ├── user-scenarios/
    │   ├── organizer-scenario.js    # Escenario organizador
    │   ├── author-scenario.js       # Escenario autor
    │   └── reviewer-scenario.js     # Escenario revisor
    └── error-handling/
        ├── form-errors.test.js      # Manejo errores formularios
        └── network-errors.test.js   # Manejo errores red

test-config/
├── jest.config.js              # Configuración Jest
├── playwright.config.js        # Configuración Playwright
├── cypress.config.js           # Configuración Cypress
├── puppeteer.config.js         # Configuración Puppeteer
└── lighthouse.config.js        # Configuración Lighthouse
```

**✅ TAREAS:**
- [ ] Configurar entorno de testing (Jest, Playwright, Cypress)
- [ ] Crear tests unitarios para todos los componentes
- [ ] Implementar tests de integración para flujos críticos
- [ ] Realizar testing visual regression
- [ ] Implementar tests de responsive design
- [ ] Validar accesibilidad con axe-core y tests manuales
- [ ] Crear tests de performance con Lighthouse
- [ ] Realizar testing de usabilidad con usuarios reales
- [ ] Implementar tests de carga y stress
- [ ] Crear suite de tests automatizados para CI/CD

#### **7.2 Documentación**

**🆕 ARCHIVOS A CREAR:**
```
frontend_docs/
├── design-system/
│   ├── design-system.md        # Sistema de diseño completo
│   ├── colors.md               # Paleta de colores
│   ├── typography.md           # Sistema tipográfico
│   ├── spacing.md              # Sistema de espaciado
│   ├── icons.md                # Librería de iconos
│   └── animations.md           # Guía de animaciones
├── components/
│   ├── component-library.md    # Librería de componentes
│   ├── buttons/
│   │   ├── buttons.md          # Documentación botones
│   │   ├── examples.html       # Ejemplos de uso
│   │   └── code-snippets.md    # Snippets de código
│   ├── forms/
│   │   ├── forms.md            # Documentación formularios
│   │   ├── validation.md       # Guía validación
│   │   └── accessibility.md    # Accesibilidad formularios
│   ├── tables/
│   │   ├── tables.md           # Documentación tablas
│   │   ├── responsive.md       # Tablas responsive
│   │   └── interactions.md     # Interacciones tablas
│   ├── cards/
│   │   ├── cards.md            # Documentación cards
│   │   └── variations.md       # Variaciones cards
│   └── navigation/
│       ├── navigation.md       # Documentación navegación
│       ├── breadcrumbs.md      # Breadcrumbs
│       └── sidebar.md          # Menú lateral
├── patterns/
│   ├── layout-patterns.md      # Patrones de layout
│   ├── interaction-patterns.md # Patrones de interacción
│   ├── data-patterns.md        # Patrones de datos
│   └── error-patterns.md       # Patrones de errores
├── guidelines/
│   ├── development-guide.md    # Guía de desarrollo
│   ├── code-standards.md       # Estándares de código
│   ├── performance-guide.md    # Guía de performance
│   ├── accessibility-guide.md  # Guía de accesibilidad
│   └── testing-guide.md        # Guía de testing
├── templates/
│   ├── page-templates.md       # Templates de páginas
│   ├── email-templates.md      # Templates de email
│   └── error-pages.md          # Páginas de error
├── assets/
│   ├── screenshots/            # Screenshots componentes
│   ├── demos/                  # Demos interactivas
│   ├── mockups/                # Mockups de diseño
│   └── style-tiles/            # Style tiles
└── changelog/
    ├── frontend-changelog.md   # Changelog frontend
    ├── migration-guides/       # Guías migración
    │   ├── v1-to-v2.md
    │   └── component-updates.md
    └── release-notes/          # Notas de versión
        ├── v2.0.0.md
        └── v2.1.0.md

storybook/
├── .storybook/
│   ├── main.js                 # Configuración Storybook
│   ├── preview.js              # Preview Storybook
│   └── manager.js              # Manager Storybook
├── stories/
│   ├── components/
│   │   ├── Button.stories.js   # Stories botones
│   │   ├── Form.stories.js     # Stories formularios
│   │   ├── Table.stories.js    # Stories tablas
│   │   └── Card.stories.js     # Stories cards
│   ├── pages/
│   │   ├── Dashboard.stories.js # Stories dashboards
│   │   └── Auth.stories.js     # Stories autenticación
│   └── patterns/
│       ├── Layout.stories.js   # Stories layouts
│       └── Navigation.stories.js # Stories navegación
└── docs/
    ├── introduction.stories.mdx # Introducción
    ├── getting-started.stories.mdx # Comenzar
    └── guidelines.stories.mdx   # Guías
```

**✅ TAREAS:**
- [ ] Crear sistema de diseño completo documentado
- [ ] Desarrollar librería de componentes con Storybook
- [ ] Documentar todos los patrones y guidelines
- [ ] Crear guías de desarrollo frontend detalladas
- [ ] Implementar demos interactivas de componentes
- [ ] Documentar proceso de testing y QA
- [ ] Crear guías de migración y actualización
- [ ] Establecer proceso de versionado de componentes
- [ ] Crear templates y boilerplates para desarrollo
- [ ] Documentar mejores prácticas y estándares de código

## 🛠️ HERRAMIENTAS Y TECNOLOGÍAS

### **Frameworks y Librerías**
- **Bootstrap 5.3+**: Framework CSS base
- **Font Awesome/Bootstrap Icons**: Iconografía
- **Chart.js**: Gráficos y métricas
- **Animate.css**: Animaciones sutiles

### **Herramientas de Desarrollo**
- **PostCSS**: Procesamiento de CSS
- **PurgeCSS**: Eliminación de CSS no usado
- **Sass/SCSS**: Preprocesador CSS (opcional)
- **Gulp/Webpack**: Automatización de tareas

### **Testing y Validación**
- **Lighthouse**: Auditoría de performance
- **axe-core**: Testing de accesibilidad
- **BrowserStack**: Testing cross-browser
- **Selenium**: Testing automatizado (ya existente)

## 📊 MÉTRICAS DE ÉXITO

### **Métricas Técnicas**
- **Performance Score**: >90 en Lighthouse
- **Accessibility Score**: >95 en axe-core
- **SEO Score**: >90 en Lighthouse
- **Mobile Usability**: 100% responsive

### **Métricas de Usuario**
- **Tiempo de Carga**: <3 segundos en 3G
- **Task Success Rate**: >95% en tareas críticas
- **User Satisfaction**: >8/10 en encuestas
- **Error Rate**: <2% en formularios principales

### **Métricas de Código**
- **CSS Size**: Reducción >30% del CSS actual
- **JavaScript Errors**: 0 errores críticos
- **Cross-browser Compatibility**: 100% en navegadores objetivo
- **Maintenance Score**: Código reutilizable y documentado

## 🎯 ENTREGABLES FINALES

1. **Sistema de Diseño Completo**: Documentación de colores, tipografía, espaciado
2. **Librería de Componentes**: Componentes reutilizables documentados
3. **Templates Rediseñados**: 25+ vistas mejoradas y optimizadas
4. **Guías de Desarrollo**: Documentación para futuros desarrolladores
5. **Kit de Branding UAZ**: Recursos visuales institucionales integrados

---

## 💡 CONSIDERACIONES ESPECIALES

### **Identidad Académica**
- Usar terminología académica apropiada
- Incorporar elementos visuales universitarios
- Mantener profesionalismo y seriedad
- Reflejar valores institucionales de UAZ

### **Usabilidad Académica**
- Priorizar eficiencia en tareas repetitivas
- Minimizar clics para acciones comunes
- Proporcionar feedback claro en cada acción
- Facilitar trabajo colaborativo entre roles

### **Escalabilidad**
- Diseñar para crecimiento futuro
- Mantener flexibilidad en componentes
- Documentar patrones para nuevos desarrolladores
- Establecer convenciones claras

---

## 📊 RESUMEN DE ARCHIVOS POR FASE

### **TOTALES GENERALES**
- **🆕 Archivos a Crear**: ~180 archivos nuevos
- **🔄 Archivos a Modificar**: ~25 templates existentes
- **📁 Nuevas Carpetas**: ~35 directorios
- **⚖️ Ratio Nuevo/Modificado**: 88% nuevo código

### **BREAKDOWN POR FASE**

#### **FASE 1: Fundación (Archivos: 45)**
- **CSS Core**: 8 archivos
- **Templates Base**: 12 archivos
- **Componentes**: 20 archivos
- **JavaScript**: 5 archivos

#### **FASE 2: Autenticación (Archivos: 18)**
- **Templates Auth**: 8 archivos modificados
- **Componentes Auth**: 6 archivos nuevos
- **Assets**: 4 archivos

#### **FASE 3: Dashboards (Archivos: 25)**
- **Templates Dashboard**: 5 archivos modificados
- **Componentes**: 16 archivos nuevos
- **JavaScript**: 4 archivos

#### **FASE 4: Conferencias (Archivos: 22)**
- **Templates**: 7 archivos modificados
- **Componentes**: 11 archivos nuevos
- **Assets**: 4 archivos

#### **FASE 5: Evaluación (Archivos: 28)**
- **Templates**: 4 archivos modificados
- **Componentes**: 20 archivos nuevos
- **JavaScript**: 4 archivos

#### **FASE 6: Optimización (Archivos: 35)**
- **Build Tools**: 15 archivos
- **Optimización**: 10 archivos
- **Configuración**: 10 archivos

#### **FASE 7: Testing y Docs (Archivos: 85)**
- **Tests**: 45 archivos
- **Documentación**: 35 archivos
- **Storybook**: 5 archivos

---

## 🎯 CHECKLIST DE MIGRACIÓN

### **Pre-Desarrollo**
- [ ] Backup completo del proyecto actual
- [ ] Configurar entorno de desarrollo
- [ ] Instalar herramientas necesarias
- [ ] Crear rama de desarrollo `frontend-redesign`

### **Por Cada Fase**
- [ ] Crear estructura de carpetas
- [ ] Implementar archivos nuevos
- [ ] Modificar templates existentes
- [ ] Ejecutar tests
- [ ] Validar en múltiples navegadores
- [ ] Code review

### **Post-Desarrollo**
- [ ] Testing completo del sistema
- [ ] Validación de accesibilidad
- [ ] Optimización de performance
- [ ] Documentación final
- [ ] Deploy a producción

---

**Documento creado para guiar el rediseño frontend del sistema CORA - UAZ**  
**Versión 2.0 Expandida | Fecha: Enero 2025**  
**Total de archivos especificados: ~200 archivos | 7 fases | 10 semanas**