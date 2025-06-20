from django.conf import settings
from django.db import models


class Notificacion(models.Model):
    """
    Modelo que representa una notificación para un usuario.

    Attributes:
        usuario (ForeignKey): Usuario destinatario de la notificación.
        mensaje (CharField): Texto del mensaje de la notificación.
        leida (BooleanField): Indica si la notificación ha sido leída. Por defecto es False.
        fecha (DateTimeField): Fecha y hora en que se creó la notificación, asignada automáticamente.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.mensaje}"
