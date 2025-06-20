from django.contrib.auth.models import AbstractUser
from django.db import models

# Áreas de conocimiento
AREAS_CONOCIMIENTO = [
    ('Ingenieria', 'Ingeniería'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser para incluir
    áreas de conocimiento y usar el correo como username.

    Attributes:
        area_conocimiento (CharField): Área de conocimiento del usuario.
        nombre (CharField): Nombre del usuario.
        apellidos (CharField): Apellidos del usuario.
        email (EmailField): Correo electrónico único del usuario.
        username (EmailField): Correo electrónico usado como nombre de usuario único.
    """

    area_conocimiento = models.CharField(
        max_length=50, choices=AREAS_CONOCIMIENTO)

    # Utilizamos los campos heredados de AbstractUser para nombre y apellidos
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    username = models.EmailField(unique=True)  # Usamos el correo como username

    def __str__(self):
        """
        Retorna una representación en string del usuario.

        Returns:
            str: Nombre completo seguido del username entre paréntesis.
        """
        return f"{self.nombre} {self.apellidos} ({self.username})"

    @property
    def conferencias_como_revisor(self):
        """
        Obtiene las conferencias donde el usuario ha sido invitado como revisor
        y su invitación ha sido aceptada.

        Returns:
            QuerySet: Conferencias con estado de invitación 'aceptado' para este usuario.
        """
        from conferencia.models import Conferencia
        return Conferencia.objects.filter(
            invitaciones_revisor__autor=self,
            invitaciones_revisor__estado='aceptado'
        )
