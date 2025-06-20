from django.conf import settings  # para usar AUTH_USER_MODEL
from django.db import models
from django.core.validators import FileExtensionValidator

AREAS_CONOCIMIENTO = [
    ('Ingenieria', 'Ingeniería'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]


class Conferencia(models.Model):
    """Modelo que representa una conferencia registrada en el sistema.

    Atributos:
        nombre (str): Nombre de la conferencia.
        meses (int): Duración en meses.
        dias (int): Duración en días.
        horas (int): Duración en horas.
        minutos (int): Duración en minutos.
        organizador (User): Usuario que organiza la conferencia.
        categoria (str): Área de conocimiento de la conferencia.
        estado_revision (str): Estado de revisión ('aceptado' o 'rechazado').
        trabajo_reportado (bool): Indica si se ha reportado un trabajo.
        autor (User): Autor de la conferencia.
        archivo_zip (File): Archivo ZIP asociado, validado por su extensión.

    Métodos:
        __str__(): Devuelve el nombre de la conferencia.
        invitaciones(): Propiedad que retorna las invitaciones asociadas a esta conferencia.
    """
    nombre = models.CharField(max_length=255)
    meses = models.IntegerField(default=0)
    dias = models.IntegerField(default=0)
    horas = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)

    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conferencias_organizadas'
    )

    categoria = models.CharField(max_length=50, choices=AREAS_CONOCIMIENTO)

    estado_revision = models.CharField(
        max_length=20,
        choices=[("aceptado", "Aceptado"), ("rechazado", "Rechazado")],
        blank=True,
        null=True
    )

    trabajo_reportado = models.BooleanField(default=False)

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conferencias_autorias'
    )

    archivo_zip = models.FileField(
        upload_to='conferencias_zips/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['zip'])]
    )

    def __str__(self):
        """Devuelve una representación legible del objeto."""
        return self.nombre

    @property
    def invitaciones(self):
        """Consulta las invitaciones de revisores asociadas a esta conferencia.

        Returns:
            QuerySet: Lista de objetos InvitacionRevisor relacionados.
        """
        return InvitacionRevisor.objects.filter(conferencia=self)


class InvitacionRevisor(models.Model):
    """Modelo que representa una invitación a un revisor para evaluar una conferencia.

    Atributos:
        conferencia (Conferencia): Conferencia a la que se envía la invitación.
        autor (User): Usuario invitado como revisor.
        estado (str): Estado de la invitación ('pendiente', 'aceptado', 'rechazado').
        fecha_envio (datetime): Fecha y hora de creación de la invitación.

    Métodos:
        __str__(): Devuelve una representación legible de la invitación.
    """
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    conferencia = models.ForeignKey(
        Conferencia,
        on_delete=models.CASCADE,
        related_name='invitaciones_revisor'  # <--- ESTA LÍNEA ES NUEVA
    )

    autor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    estado = models.CharField(
        max_length=10, choices=ESTADOS, default='pendiente')

    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devuelve una representación legible del objeto."""
        return f"{self.autor.nombre} - {self.conferencia.nombre} ({self.estado})"
