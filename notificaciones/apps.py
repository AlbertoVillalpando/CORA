from django.apps import AppConfig


class NotificacionesConfig(AppConfig):
    """
    Configuración de la aplicación 'notificaciones' para Django.

    Attributes:
        default_auto_field (str): Tipo de campo automático usado por defecto para los modelos.
        name (str): Nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notificaciones'
