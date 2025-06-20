# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CORA is a Conference Paper Review Management System (similar to EasyChair) built with Django. It manages the complete academic conference review process from paper submission to final evaluation.

## Development Commands

### Running the Application
```bash
# Start development environment
docker network create proxy
docker-compose up -d --build

# Access the application at http://localhost:8000
```

### Testing
```bash
# Run all tests with coverage (95% minimum required)
coverage run --branch --source='.' --omit="*/migrations/*,*test*,*__init__*,*settings*,*apps*,*wsgi.py*,*admin.py*,*asgi.py*,*manage.py*,*urls.py*" manage.py test

# Generate coverage report
coverage report -m --fail-under 95

# Generate HTML coverage report
coverage html

# Run specific app tests
python manage.py test usuarios
python manage.py test conferencia
python manage.py test formulario

# Run acceptance tests (BDD with Behave)
behave pruebas_aceptacion/CORA/features/
```

### Code Quality
```bash
# Run linting
flake8 .
```

## Architecture Overview

### Core Django Apps
- **usuarios**: User management with role-based access (Admin, Organizador, Autor, Revisor)
- **conferencia**: Conference and paper submission management
- **formulario**: Dynamic evaluation forms and review system
- **notificaciones**: User notification system
- **home**: Landing page and dashboards

### Key Models and Relationships
- **CustomUser**: Email-based authentication with knowledge areas (Ingeniería, Medicina, Letras, Contabilidad)
- **Conferencia**: Paper submissions with organizer/author relationships, ZIP file uploads
- **InvitacionRevisor**: Reviewer invitation workflow (pending/accepted/rejected)
- **Evaluacion/Pregunta/Respuesta**: Dynamic review forms with 1-5 scoring system

### User Roles and Workflow
1. **Organizador**: Creates conferences, invites reviewers
2. **Autor**: Submits papers as ZIP files
3. **Revisor**: Evaluates papers using dynamic forms
4. **Admin**: System administration

### Database Setup
- Development: SQLite3 (db.sqlite3)
- Production: MariaDB in Docker container
- Migrations are managed in each app's migrations/ directory

## Test Users (for development)
- Administrator: `adminP@adminP.com` / `P123456789`
- Organizer: `organizadorP@organizadorP.com` / `P123456789`
- Reviewer: `revisorP@revisorP.com` / `P123456789`
- Author: `autorP@autorP.com` / `P123456789`

## File Upload Handling
- Conference papers uploaded as ZIP files to `media/conferencias_zips/`
- Django handles file naming conflicts with automatic suffixes

## Testing Requirements
- Minimum 95% code coverage required
- Unit tests for all models, forms, and views
- BDD acceptance tests using Behave + Selenium
- Test files exclude migrations, settings, and admin files from coverage

## Deployment
- Dockerized application with docker-compose.yml
- Uses custom proxy network for container communication
- MariaDB with persistent volume for production data