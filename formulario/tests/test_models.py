from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from formulario.models import Evaluacion, Pregunta, Respuesta
from conferencia.models import Conferencia

User = get_user_model()


class EvaluacionModelTest(TestCase):
    def setUp(self):
        self.user_organizador = User.objects.create_user(
            username='organizador@example.com',
            email='organizador@example.com',
            password='testpass123',
            nombre='Organizador',
            apellidos='Test',
            area_conocimiento='Ingenieria'
        )

        self.user_revisor = User.objects.create_user(
            username='revisor@example.com',
            email='revisor@example.com',
            password='testpass123',
            nombre='Revisor',
            apellidos='Test',
            area_conocimiento='Medicina'
        )

        self.conferencia = Conferencia.objects.create(
            nombre='Test Conference',
            organizador=self.user_organizador,
            categoria='Ingenieria'
        )

    def test_evaluacion_creation(self):
        """Test basic evaluation creation"""
        evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor,
            retroalimentacion='Excelente trabajo'
        )

        self.assertEqual(evaluacion.conferencia, self.conferencia)
        self.assertEqual(evaluacion.revisor, self.user_revisor)
        self.assertEqual(evaluacion.retroalimentacion, 'Excelente trabajo')

    def test_evaluacion_str_method(self):
        """Test string representation of evaluation"""
        evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        expected_str = f"Evaluación de {self.user_revisor} para {self.conferencia}"
        self.assertEqual(str(evaluacion), expected_str)

    def test_evaluacion_unique_together_constraint(self):
        """Test unique_together constraint for conferencia and revisor"""
        # Create first evaluation
        Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        # Attempt to create second evaluation with same conferencia and revisor
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Evaluacion.objects.create(
                    conferencia=self.conferencia,
                    revisor=self.user_revisor
                )

    def test_evaluacion_retroalimentacion_optional(self):
        """Test that retroalimentacion field is optional"""
        evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        self.assertIsNone(evaluacion.retroalimentacion)

    def test_evaluacion_retroalimentacion_blank_and_null(self):
        """Test retroalimentacion can be blank and null"""
        # Test with None
        evaluacion1 = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor,
            retroalimentacion=None
        )
        self.assertIsNone(evaluacion1.retroalimentacion)

        # Test with empty string
        user_revisor2 = User.objects.create_user(
            username='revisor2@example.com',
            email='revisor2@example.com',
            password='testpass123',
            nombre='Revisor2',
            apellidos='Test',
            area_conocimiento='Letras'
        )

        evaluacion2 = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=user_revisor2,
            retroalimentacion=''
        )
        self.assertEqual(evaluacion2.retroalimentacion, '')

    def test_evaluacion_cascade_delete_conferencia(self):
        """Test evaluation is deleted when conference is deleted"""
        evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        evaluacion_id = evaluacion.id
        self.conferencia.delete()

        with self.assertRaises(Evaluacion.DoesNotExist):
            Evaluacion.objects.get(id=evaluacion_id)

    def test_evaluacion_cascade_delete_revisor(self):
        """Test evaluation is deleted when reviewer is deleted"""
        evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        evaluacion_id = evaluacion.id
        self.user_revisor.delete()

        with self.assertRaises(Evaluacion.DoesNotExist):
            Evaluacion.objects.get(id=evaluacion_id)


class PreguntaModelTest(TestCase):
    def setUp(self):
        self.user_organizador = User.objects.create_user(
            username='organizador@example.com',
            email='organizador@example.com',
            password='testpass123',
            nombre='Organizador',
            apellidos='Test',
            area_conocimiento='Ingenieria'
        )

        self.conferencia = Conferencia.objects.create(
            nombre='Test Conference',
            organizador=self.user_organizador,
            categoria='Ingenieria'
        )

    def test_pregunta_creation(self):
        """Test basic question creation"""
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='¿Cuál es la calidad del trabajo?'
        )

        self.assertEqual(pregunta.conferencia, self.conferencia)
        self.assertEqual(pregunta.texto, '¿Cuál es la calidad del trabajo?')

    def test_pregunta_str_method(self):
        """Test string representation of question"""
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='¿Es innovador el proyecto?'
        )

        self.assertEqual(str(pregunta), '¿Es innovador el proyecto?')

    def test_pregunta_texto_max_length(self):
        """Test texto field max length constraint"""
        long_text = 'a' * 256  # 256 characters, exceeds max_length=255

        with self.assertRaises(ValidationError):
            pregunta = Pregunta(
                conferencia=self.conferencia,
                texto=long_text
            )
            pregunta.full_clean()

    def test_pregunta_texto_exact_max_length(self):
        """Test texto field with exactly max length"""
        exact_length_text = 'a' * 255  # Exactly 255 characters

        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto=exact_length_text
        )

        self.assertEqual(len(pregunta.texto), 255)
        self.assertEqual(pregunta.texto, exact_length_text)

    def test_pregunta_related_name_preguntas(self):
        """Test related_name 'preguntas' works correctly"""
        pregunta1 = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='Pregunta 1'
        )

        pregunta2 = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='Pregunta 2'
        )

        preguntas = self.conferencia.preguntas.all()
        self.assertEqual(preguntas.count(), 2)
        self.assertIn(pregunta1, preguntas)
        self.assertIn(pregunta2, preguntas)

    def test_pregunta_cascade_delete_conferencia(self):
        """Test question is deleted when conference is deleted"""
        pregunta = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='Test question'
        )

        pregunta_id = pregunta.id
        self.conferencia.delete()

        with self.assertRaises(Pregunta.DoesNotExist):
            Pregunta.objects.get(id=pregunta_id)


class RespuestaModelTest(TestCase):
    def setUp(self):
        self.user_organizador = User.objects.create_user(
            username='organizador@example.com',
            email='organizador@example.com',
            password='testpass123',
            nombre='Organizador',
            apellidos='Test',
            area_conocimiento='Ingenieria'
        )

        self.user_revisor = User.objects.create_user(
            username='revisor@example.com',
            email='revisor@example.com',
            password='testpass123',
            nombre='Revisor',
            apellidos='Test',
            area_conocimiento='Medicina'
        )

        self.conferencia = Conferencia.objects.create(
            nombre='Test Conference',
            organizador=self.user_organizador,
            categoria='Ingenieria'
        )

        self.evaluacion = Evaluacion.objects.create(
            conferencia=self.conferencia,
            revisor=self.user_revisor
        )

        self.pregunta = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='¿Cuál es la calidad?'
        )

    def test_respuesta_creation(self):
        """Test basic answer creation"""
        respuesta = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=4
        )

        self.assertEqual(respuesta.evaluacion, self.evaluacion)
        self.assertEqual(respuesta.pregunta, self.pregunta)
        self.assertEqual(respuesta.puntaje, 4)

    def test_respuesta_str_method(self):
        """Test string representation of answer"""
        respuesta = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=3
        )

        expected_str = f"{self.pregunta} - 3"
        self.assertEqual(str(respuesta), expected_str)

    def test_respuesta_puntaje_choices_valid(self):
        """Test valid puntaje choices (1-5)"""
        for puntaje in range(1, 6):
            respuesta = Respuesta.objects.create(
                evaluacion=self.evaluacion,
                pregunta=self.pregunta,
                puntaje=puntaje
            )
            self.assertEqual(respuesta.puntaje, puntaje)
            respuesta.delete()  # Clean up for next iteration

    def test_respuesta_puntaje_choices_invalid_low(self):
        """Test invalid puntaje choice (below 1)"""
        with self.assertRaises(ValidationError):
            respuesta = Respuesta(
                evaluacion=self.evaluacion,
                pregunta=self.pregunta,
                puntaje=0
            )
            respuesta.full_clean()

    def test_respuesta_puntaje_choices_invalid_high(self):
        """Test invalid puntaje choice (above 5)"""
        with self.assertRaises(ValidationError):
            respuesta = Respuesta(
                evaluacion=self.evaluacion,
                pregunta=self.pregunta,
                puntaje=6
            )
            respuesta.full_clean()

    def test_respuesta_related_name_respuestas(self):
        """Test related_name 'respuestas' works correctly"""
        respuesta1 = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=4
        )

        pregunta2 = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='Segunda pregunta'
        )

        respuesta2 = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=pregunta2,
            puntaje=5
        )

        respuestas = self.evaluacion.respuestas.all()
        self.assertEqual(respuestas.count(), 2)
        self.assertIn(respuesta1, respuestas)
        self.assertIn(respuesta2, respuestas)

    def test_respuesta_cascade_delete_evaluacion(self):
        """Test answer is deleted when evaluation is deleted"""
        respuesta = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=3
        )

        respuesta_id = respuesta.id
        self.evaluacion.delete()

        with self.assertRaises(Respuesta.DoesNotExist):
            Respuesta.objects.get(id=respuesta_id)

    def test_respuesta_cascade_delete_pregunta(self):
        """Test answer is deleted when question is deleted"""
        respuesta = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=3
        )

        respuesta_id = respuesta.id
        self.pregunta.delete()

        with self.assertRaises(Respuesta.DoesNotExist):
            Respuesta.objects.get(id=respuesta_id)

    def test_multiple_respuestas_same_evaluacion(self):
        """Test multiple answers for the same evaluation"""
        pregunta2 = Pregunta.objects.create(
            conferencia=self.conferencia,
            texto='Segunda pregunta'
        )

        respuesta1 = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=self.pregunta,
            puntaje=4
        )

        respuesta2 = Respuesta.objects.create(
            evaluacion=self.evaluacion,
            pregunta=pregunta2,
            puntaje=2
        )

        respuestas = Respuesta.objects.filter(evaluacion=self.evaluacion)
        self.assertEqual(respuestas.count(), 2)
        self.assertIn(respuesta1, respuestas)
        self.assertIn(respuesta2, respuestas)
