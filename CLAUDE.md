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

## Security Configuration
- Environment variables managed with django-environ
- Security headers configured for production (HSTS, XSS, CSRF protection)
- CSRF protection properly implemented (no @csrf_exempt bypass)
- HTTPS redirect enabled for production
- Secure logging system for security events
- Production settings separated from development

## Deployment

### Quick Setup (Development)
```bash
# Automated development setup
./scripts/setup-dev.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Production Deployment
```bash
# Automated production deployment
./scripts/deploy-production.sh

# Manual deployment
pip install -r requirements.txt
cp .env.production .env.production.local
# Configure production variables in .env.production.local
export DJANGO_SETTINGS_MODULE=cora.settings_production
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic
```

### Environment Variables
- **Required**: SECRET_KEY, DEBUG, ALLOWED_HOSTS
- **Security**: SECURE_SSL_REDIRECT, CSRF_TRUSTED_ORIGINS
- **Database**: DB_NAME, DB_USER, DB_PASSWORD (production)
- **Email**: EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
- See `.env.example` for complete list

### Security Features
- SECRET_KEY from environment (not hardcoded)
- DEBUG=False enforced in production
- HTTPS security headers (HSTS, XSS protection)
- CSRF protection without unsafe bypasses
- Secure cookie settings for production
- Security event logging to `logs/security.log`

### Docker Configuration
- Development: `docker-compose up -d --build`
- Production: `docker-compose -f docker-compose.prod.yml up -d`
- Uses custom proxy network for container communication
- MariaDB with persistent volume for production data
- Environment-based configuration