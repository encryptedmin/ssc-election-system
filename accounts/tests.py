from django.test import TestCase, override_settings
from django.urls import reverse

from .models import User


@override_settings(SECURE_SSL_REDIRECT=False)
class AdminRegistrationApprovalTests(TestCase):

    def test_admin_registration_creates_pending_admin(self):
        response = self.client.post(
            reverse('admin_register'),
            {
                'username': 'pendingadmin',
                'email': 'pending@example.com',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            },
        )

        self.assertRedirects(response, reverse('login'))

        admin = User.objects.get(username='pendingadmin')
        self.assertEqual(admin.role, 'ADMIN')
        self.assertFalse(admin.is_approved)

    def test_pending_admin_cannot_login_until_masteradmin_approves(self):
        admin = User.objects.create_user(
            username='pendingadmin',
            email='pending@example.com',
            password='StrongPass12345',
            role='ADMIN',
            is_approved=False,
        )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'pendingadmin',
                'password': 'StrongPass12345',
            },
        )

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

        masteradmin = User.objects.get(username='masteradmin')
        self.client.force_login(masteradmin)

        self.client.post(reverse('approve_user', args=[admin.id]))
        admin.refresh_from_db()

        self.assertTrue(admin.is_approved)

        self.client.logout()
        response = self.client.post(
            reverse('login'),
            {
                'username': 'pendingadmin',
                'password': 'StrongPass12345',
            },
        )

        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_approved_admin_cannot_access_approval_dashboard(self):
        admin = User.objects.create_user(
            username='approvedadmin',
            email='approved@example.com',
            password='StrongPass12345',
            role='ADMIN',
            is_approved=True,
        )
        self.client.force_login(admin)

        response = self.client.get(reverse('approval_dashboard'))

        self.assertEqual(response.status_code, 302)
