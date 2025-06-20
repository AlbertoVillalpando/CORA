from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from notificaciones.models import Notificacion

User = get_user_model()


class NotificacionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123',
            nombre='Test',
            apellidos='User',
            area_conocimiento='Ingenieria'
        )

    def test_notificacion_creation(self):
        """Test basic notification creation"""
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Test notification message'
        )

        self.assertEqual(notificacion.usuario, self.user)
        self.assertEqual(notificacion.mensaje, 'Test notification message')
        self.assertFalse(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha)
        self.assertIsInstance(notificacion.fecha, timezone.datetime)

    def test_notificacion_str_method(self):
        """Test string representation of notification"""
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Test message'
        )
        expected_str = f"Notificación para {self.user.username}: Test message"
        self.assertEqual(str(notificacion), expected_str)

    def test_notificacion_default_values(self):
        """Test default values for notification fields"""
        notificacion = Notificacion()
        notificacion.usuario = self.user
        notificacion.mensaje = 'Test'
        notificacion.save()

        self.assertFalse(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha)

    def test_notificacion_leida_field(self):
        """Test leida field functionality"""
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Test message'
        )

        # Should be False by default
        self.assertFalse(notificacion.leida)

        # Update to True
        notificacion.leida = True
        notificacion.save()
        notificacion.refresh_from_db()
        self.assertTrue(notificacion.leida)

    def test_notificacion_usuario_cascade_delete(self):
        """Test that notification is deleted when user is deleted"""
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Test message'
        )

        notificacion_id = notificacion.id
        self.user.id

        # Delete user
        self.user.delete()

        # Notification should be deleted too
        with self.assertRaises(Notificacion.DoesNotExist):
            Notificacion.objects.get(id=notificacion_id)

    def test_notificacion_mensaje_max_length(self):
        """Test mensaje field max length constraint"""
        long_message = 'a' * 256  # 256 characters, exceeds max_length=255

        with self.assertRaises(ValidationError):
            notificacion = Notificacion(
                usuario=self.user,
                mensaje=long_message
            )
            notificacion.full_clean()

    def test_notificacion_mensaje_exact_max_length(self):
        """Test mensaje field with exactly max length"""
        exact_length_message = 'a' * 255  # Exactly 255 characters

        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje=exact_length_message
        )

        self.assertEqual(len(notificacion.mensaje), 255)
        self.assertEqual(notificacion.mensaje, exact_length_message)

    def test_notificacion_fecha_auto_now_add(self):
        """Test that fecha is automatically set on creation"""
        before_creation = timezone.now()

        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Test message'
        )

        after_creation = timezone.now()

        self.assertGreaterEqual(notificacion.fecha, before_creation)
        self.assertLessEqual(notificacion.fecha, after_creation)

    def test_notificacion_fecha_not_updated_on_save(self):
        """Test that fecha is not updated when saving existing notification"""
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Original message'
        )

        original_fecha = notificacion.fecha

        # Wait a bit and update
        import time
        time.sleep(0.01)

        notificacion.mensaje = 'Updated message'
        notificacion.save()
        notificacion.refresh_from_db()

        self.assertEqual(notificacion.fecha, original_fecha)

    def test_multiple_notifications_for_same_user(self):
        """Test creating multiple notifications for the same user"""
        notificacion1 = Notificacion.objects.create(
            usuario=self.user,
            mensaje='First notification'
        )

        notificacion2 = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Second notification'
        )

        user_notifications = Notificacion.objects.filter(usuario=self.user)
        self.assertEqual(user_notifications.count(), 2)
        self.assertIn(notificacion1, user_notifications)
        self.assertIn(notificacion2, user_notifications)

    def test_notification_ordering_by_fecha(self):
        """Test notifications can be ordered by fecha"""
        # Create notifications with slight time differences
        notificacion1 = Notificacion.objects.create(
            usuario=self.user,
            mensaje='First notification'
        )

        import time
        time.sleep(0.01)

        notificacion2 = Notificacion.objects.create(
            usuario=self.user,
            mensaje='Second notification'
        )

        # Order by fecha ascending
        notifications_asc = list(Notificacion.objects.filter(
            usuario=self.user).order_by('fecha'))
        self.assertEqual(notifications_asc[0], notificacion1)
        self.assertEqual(notifications_asc[1], notificacion2)

        # Order by fecha descending
        notifications_desc = list(Notificacion.objects.filter(
            usuario=self.user).order_by('-fecha'))
        self.assertEqual(notifications_desc[0], notificacion2)
        self.assertEqual(notifications_desc[1], notificacion1)
