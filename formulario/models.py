from django.db import models
from conferencia.models import Conferencia
from django.conf import settings


class Evaluacion(models.Model):
    """
    Modelo que representa la evaluación realizada por un revisor a una conferencia.

    Attributes:
        conferencia (ForeignKey): Referencia a la conferencia evaluada.
        revisor (ForeignKey): Usuario que realiza la evaluación.
        retroalimentacion (TextField): Comentarios o retroalimentación opcional sobre la conferencia.
    """
    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE)
    revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    retroalimentacion = models.TextField(blank=True, null=True)

    class Meta:
        """
        Metadatos del modelo.

        Attributes:
            unique_together (tuple): Asegura que un revisor solo pueda evaluar una conferencia una vez.
        """
        unique_together = ('conferencia', 'revisor')

    def __str__(self):
        """
        Representación en cadena del modelo.

        Returns:
            str: Una descripción legible de la evaluación.
        """
        return f"Evaluación de {self.revisor} para {self.conferencia}"


class Pregunta(models.Model):
    """
    Modelo que representa una pregunta asociada a una conferencia.

    Attributes:
        conferencia (ForeignKey): Referencia a la conferencia a la que pertenece la pregunta.
        texto (CharField): Texto de la pregunta con un máximo de 255 caracteres.
    """

    conferencia = models.ForeignKey(
        Conferencia, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        """
        Representación en cadena del modelo.

        Returns:
            str: El texto de la pregunta.
        """
        return self.texto


class Respuesta(models.Model):
    """
    Modelo que representa una respuesta a una pregunta dentro de una evaluación.

    Attributes:
        evaluacion (ForeignKey): Referencia a la evaluación a la que pertenece esta respuesta.
        pregunta (ForeignKey): Pregunta a la que se está respondiendo.
        puntaje (IntegerField): Puntaje asignado a la respuesta, valor entre 1 y 5.
    """

    evaluacion = models.ForeignKey(
        Evaluacion, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    puntaje = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        """
        Representación en cadena del modelo.

        Returns:
            str: Texto de la pregunta seguido del puntaje asignado.
        """
        return f"{self.pregunta} - {self.puntaje}"
