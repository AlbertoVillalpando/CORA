from django.test import TestCase, Client
from django.urls import reverse
from conferencia.models import Conferencia
from formulario.models import Pregunta, Respuesta, Evaluacion
from notificaciones.models import Notificacion
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from conferencia.models import InvitacionRevisor
User = get_user_model()


class FormularioViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear usuarios de prueba
        self.usuario = User.objects.create_user(
            username='revisorP',
            email='revisorP@revisorP.com',
            password='P123456789'
        )
        self.autor = User.objects.create_user(
            username='autorP',
            email='autorP@autorP.com',
            password='P123456789'
        )

        self.admin = User.objects.create_user(
            username='adminP',
            email='adminP@adminP.com',
            password='P123456789'
        )

        # Login del revisor
        self.client.force_login(self.usuario)

        # Crear conferencia
        self.conferencia = Conferencia.objects.create(
            nombre="Conf de prueba", autor=self.autor)

        # URLs
        self.crear_url = reverse('crear_formulario', args=[
                                 self.conferencia.id])
        self.ver_url = reverse('ver_formulario', args=[self.conferencia.id])
        self.evaluar_url = reverse(
            'evaluar_conferencia', args=[self.conferencia.id])
        self.ver_eval_url = reverse(
            'ver_evaluacion', args=[self.conferencia.id])

    def test_crear_formulario_get(self):
        response = self.client.get(self.crear_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/crear_formulario.html')

    def test_crear_formulario_post_valido(self):
        self.client.post(self.crear_url, data={'preguntas': ['Pregunta 1', 'Pregunta 2']})
        self.assertEqual(Pregunta.objects.filter(
            conferencia=self.conferencia).count(), 2)

    def test_crear_formulario_post_vacio(self):
        self.client.post(self.crear_url, data={'preguntas': ['   ', '']})
        self.assertEqual(Pregunta.objects.filter(conferencia=self.conferencia).count(), 0)

    def test_ver_formulario_get(self):
        Pregunta.objects.create(
            conferencia=self.conferencia, texto="¿Cómo evalúas?")
        response = self.client.get(self.ver_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/ver_formulario.html')
        self.assertContains(response, "¿Cómo evalúas?")

    def test_ver_formulario_post_respuestas_validas(self):
        p1 = Pregunta.objects.create(conferencia=self.conferencia, texto="P1")
        p2 = Pregunta.objects.create(conferencia=self.conferencia, texto="P2")
        data = {f"respuesta_{p1.id}": "4", f"respuesta_{p2.id}": "5"}
        response = self.client.post(self.ver_url, data=data)
        self.assertEqual(Respuesta.objects.count(), 2)
        self.assertRedirects(response, reverse('home'))

    def test_ver_formulario_post_sin_respuestas(self):
        Pregunta.objects.create(conferencia=self.conferencia, texto="P1")
        self.client.post(self.ver_url, data={})
        self.assertEqual(Respuesta.objects.count(), 0)

    def test_evaluar_conferencia_get(self):
        Pregunta.objects.create(
            conferencia=self.conferencia, texto="Pregunta 1")
        response = self.client.get(self.evaluar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'formulario/evaluar_conferencia.html')

    def test_evaluar_conferencia_post(self):
        p1 = Pregunta.objects.create(
            conferencia=self.conferencia, texto="Pregunta 1")
        p2 = Pregunta.objects.create(
            conferencia=self.conferencia, texto="Pregunta 2")

        data = {
            f'respuesta_{p1.id}': '3',
            f'respuesta_{p2.id}': '4',
            'retroalimentacion': 'Buen trabajo'
        }

        response = self.client.post(self.evaluar_url, data=data)
        self.assertRedirects(response, reverse('conferencias_revisor'))

        evaluacion = Evaluacion.objects.get(
            conferencia=self.conferencia, revisor=self.usuario)
        self.assertEqual(evaluacion.retroalimentacion, 'Buen trabajo')
        self.assertEqual(evaluacion.respuestas.count(), 2)

        notificacion = Notificacion.objects.get(usuario=self.autor)
        self.assertIn("ha sido evaluada", notificacion.mensaje)

    def test_ver_evaluacion_get(self):
        Evaluacion.objects.create(
            conferencia=self.conferencia, revisor=self.usuario)
        response = self.client.get(self.ver_eval_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/ver_evaluacion.html')
        self.assertContains(response, self.conferencia.nombre)

    def test_conferencias_organizador_view(self):
        # Crea un usuario organizador
        organizador = User.objects.create_user(
            username='organizador',
            password='testpass',
        )
        self.client.force_login(organizador)
        # Crea algunas conferencias de prueba
        Conferencia.objects.create(nombre="Conf 1", categoria="Ingeniería")
        Conferencia.objects.create(nombre="Conf 2", categoria="Ingeniería")
        Conferencia.objects.create(nombre="Conf 3", categoria="Ingeniería")
        response = self.client.get(reverse('conferencias_organizador'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/conferencias_organizador.html')
        self.assertEqual(len(response.context['conferencias']), 3 + 1)

    def test_eliminar_conferencia(self):
        # Crear una conferencia de prueba
        conferencia = Conferencia.objects.create(
            nombre="Conferencia Test",
            autor=self.admin  # Asume que tienes un usuario admin en setUp
        )
        # Verificar que existe antes de eliminar
        self.assertTrue(Conferencia.objects.filter(pk=conferencia.pk).exists())
        # Llamar a la vista
        response = self.client.post(
            reverse('eliminar_conferencia', args=[conferencia.pk])
        )
        # Verificaciones
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('conferencias_administrador'))
        self.assertFalse(Conferencia.objects.filter(pk=conferencia.pk).exists())

    def test_invitar_autor_sin_seleccion(self):
        """Prueba cuando no se selecciona un autor"""
        conferencia = Conferencia.objects.create(nombre="Test Conf")
        response = self.client.post(
            reverse('invitar_autor', args=[conferencia.id]),
            data={}  # No se envía autor_id
        )
        # Verifica redirección
        self.assertRedirects(response, reverse('invitaciones_conferencia', args=[conferencia.id]))
        # Verifica mensaje de error
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("Debe seleccionar un autor", messages[0].message)

    def test_invitar_autor_exitoso(self):
        """Prueba invitación exitosa"""
        autor = User.objects.create_user(username="nuevo_autor", password='testpass')
        conferencia = Conferencia.objects.create(nombre="Test Conf", categoria="Ingeniería")
        response = self.client.post(
            reverse('invitar_autor', args=[conferencia.id]),
            data={'autor': autor.id}
        )
        # Verifica redirección
        self.assertRedirects(response, reverse('invitaciones_conferencia', args=[conferencia.id]))
        # Verifica que se creó la invitación
        self.assertTrue(InvitacionRevisor.objects.filter(
            conferencia=conferencia,
            autor=autor
        ).exists())
        # Verifica mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("invitado exitosamente", messages[0].message)

    def test_invitar_autor_inexistente(self):
        response = self.client.post(
            reverse('invitar_autor', args=[self.conferencia.id]),
            data={'autor': 9999}  # ID que no existe
        )
        self.assertEqual(response.status_code, 404)
