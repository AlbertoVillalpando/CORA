from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """
    Configuración de la aplicación 'usuarios'.

    Attributes:
        default_auto_field (str): Define el tipo de campo automático por defecto para las claves primarias.
        name (str): Nombre de la aplicación Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
