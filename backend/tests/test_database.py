from django.contrib.auth import get_user_model
from django.test import TestCase

from models.models import ClientApplication, UserConsent

User = get_user_model()


class AdminDatabasePreviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='regular@example.com',
            password='password123',
            first_name='Regular',
            last_name='User',
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
        )
        self.client_app = ClientApplication.objects.create(
            name='Portal',
            service_url='https://portal.example.com',
            redirect_uris=['https://portal.example.com/callback'],
            client_secret_hash='hashed-secret',
            signing_key_pem='private-key-pem',
            signing_cert_pem='cert-pem',
        )
        UserConsent.objects.create(
            client=self.client_app,
            user=self.user,
            granted_scopes='openid email',
        )

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/admin/database/models')
        self.assertEqual(response.status_code, 401)

    def test_requires_staff_access(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/v1/admin/database/models')
        self.assertEqual(response.status_code, 403)

        rows_response = self.client.get('/api/v1/admin/database/models/ssouser')
        self.assertEqual(rows_response.status_code, 403)

    def test_admin_can_list_all_core_models_automatically(self):
        self.client.force_login(self.admin)
        response = self.client.get('/api/v1/admin/database/models')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        keys = {m['key'] for m in data['models']}
        self.assertEqual(
            keys,
            {
                'ssouser',
                'clientapplication',
                'authorizationcode',
                'accesstoken',
                'refreshtoken',
                'userconsent',
            },
        )
        users_entry = next(m for m in data['models'] if m['key'] == 'ssouser')
        self.assertEqual(users_entry['count'], 2)

    def test_admin_can_fetch_model_rows_without_sensitive_fields(self):
        self.client.force_login(self.admin)

        users_res = self.client.get('/api/v1/admin/database/models/ssouser')
        self.assertEqual(users_res.status_code, 200)
        users_data = users_res.json()
        self.assertEqual(users_data['total_count'], 2)
        self.assertNotIn('password', users_data['rows'][0])

        clients_res = self.client.get('/api/v1/admin/database/models/clientapplication')
        self.assertEqual(clients_res.status_code, 200)
        clients_data = clients_res.json()
        self.assertEqual(clients_data['total_count'], 1)
        self.assertNotIn('client_secret_hash', clients_data['rows'][0])
        self.assertNotIn('signing_key_pem', clients_data['rows'][0])
        self.assertNotIn('signing_cert_pem', clients_data['rows'][0])

        consents_res = self.client.get('/api/v1/admin/database/models/userconsent')
        self.assertEqual(consents_res.status_code, 200)
        self.assertEqual(consents_res.json()['total_count'], 1)

    def test_unknown_model_returns_404(self):
        self.client.force_login(self.admin)
        response = self.client.get('/api/v1/admin/database/models/non-existent')
        self.assertEqual(response.status_code, 404)
