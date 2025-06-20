from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuración de la aplicación 'home'.

    Attributes:
        default_auto_field (str): Tipo de campo para la clave primaria por defecto.
        name (str): Nombre de la aplicación.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
