from django.apps import AppConfig


class ConferenciaConfig(AppConfig):
    """Configuración de la aplicación 'conferencia'.

    Esta clase configura ciertos parámetros de la aplicación Django 'conferencia',
    como el tipo de campo predeterminado para claves primarias y el nombre interno de la aplicación.

    Attributes:
        default_auto_field (str): Tipo de campo automático por defecto para claves primarias.
        name (str): Nombre interno de la aplicación, utilizado por Django para identificarla.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conferencia'
