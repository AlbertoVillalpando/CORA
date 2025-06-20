from django.test import TestCase
from django.contrib.auth import get_user_model
from formulario.models import Pregunta, Respuesta, Evaluacion
from conferencia.models import Conferencia

User = get_user_model()


class FormularioFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
            nombre='Test',
            apellidos='User',
            area_conocimiento='Ingenieria'
        )
        self.conferencia = Conferencia.objects.create(
            nombre="TestConf",
            categoria="Ingenieria"
        )
        self.evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user
        )

    def test_crear_pregunta_valida(self):
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia, texto="¿Cuál es tu experiencia?")
        self.assertEqual(pregunta.texto, "¿Cuál es tu experiencia?")
        self.assertEqual(pregunta.conferencia, self.conferencia)

    def test_crear_respuesta_valida(self):
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia, texto="¿Qué calificación das?")
        respuesta = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=pregunta,
            puntaje=4
        )
        self.assertEqual(respuesta.pregunta, pregunta)
        self.assertEqual(respuesta.evaluacion, self.evaluacion)
        self.assertEqual(respuesta.puntaje, 4)

    def test_respuesta_fuera_de_rango(self):
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia, texto="¿Qué calificación das?")
        from django.core.exceptions import ValidationError
        respuesta = Respuesta(
            evaluacion=self.evaluacion,
            pregunta=pregunta,
            puntaje=10
        )
        with self.assertRaises(ValidationError):
            respuesta.full_clean()
