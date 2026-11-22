import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from models.clients import ClientApplication
from services.crypto import (
    generate_client_secret, generate_rsa_keypair, generate_self_signed_cert,
    hash_client_secret, private_key_to_pem, verify_client_secret,
)


User = get_user_model()


class ClientApplicationApiTests(TestCase):
	def setUp(self):
		self.staff_user = User.objects.create_user(
			email='staff@example.com',
			password='Strong-Passphrase-742!',
			is_staff=True,
		)

	def payload(self, **overrides):
		data = {
			'name': 'Example service',
			'service_url': 'https://service.example.com',
			'redirect_uris': ['https://service.example.com/oidc/callback'],
		}
		data.update(overrides)
		return data

	def create_client_in_db(self, **overrides):
		"""Helper — create a ClientApplication with generated credentials."""
		fields = self.payload(**overrides)
		secret = generate_client_secret()
		key = generate_rsa_keypair()
		return ClientApplication.objects.create(
			**fields,
			client_secret_hash=hash_client_secret(secret),
			signing_key_pem=private_key_to_pem(key),
			signing_cert_pem=generate_self_signed_cert(key, fields['name']),
		)

	def post_json(self, url, data):
		return self.client.post(
			url,
			data=json.dumps(data),
			content_type='application/json',
		)

	def test_management_requires_staff(self):
		url = reverse('manage-clients')
		self.assertEqual(self.client.get(url).status_code, 401)
		self.client.force_login(
			User.objects.create_user(email='regular@example.com', password='password'),
		)
		self.assertEqual(self.client.get(url).status_code, 403)

	def test_staff_can_create_and_list_client(self):
		self.client.force_login(self.staff_user)

		created = self.post_json(reverse('manage-clients'), self.payload())

		self.assertEqual(created.status_code, 201)
		body = created.json()['client']
		self.assertEqual(len(body['client_id']), 36)

		# client_secret is returned exactly once on creation
		self.assertIn('client_secret', body)
		self.assertGreater(len(body['client_secret']), 32)

		# signing cert is populated
		self.assertTrue(body['has_signing_key'])
		self.assertIn('BEGIN CERTIFICATE', body['signing_cert_pem'])

		# secret is NOT returned in list / detail endpoints
		listed = self.client.get(reverse('manage-clients'))
		self.assertEqual(listed.status_code, 200)
		self.assertEqual(listed.json()['count'], 1)
		self.assertNotIn('client_secret', listed.json()['results'][0])

	def test_created_secret_is_verifiable(self):
		self.client.force_login(self.staff_user)

		body = self.post_json(reverse('manage-clients'), self.payload()).json()
		plain = body['client']['client_secret']
		stored = ClientApplication.objects.first()
		self.assertTrue(verify_client_secret(plain, stored.client_secret_hash))

	def test_rejects_non_https_redirect_uri_outside_localhost(self):
		self.client.force_login(self.staff_user)

		response = self.post_json(
			reverse('manage-clients'),
			self.payload(redirect_uris=['http://service.example.com/callback']),
		)

		self.assertEqual(response.status_code, 400)
		self.assertIn('redirect_uris', response.json()['errors'])

	def test_staff_can_update_client_and_delete_deactivates_it(self):
		self.client.force_login(self.staff_user)
		client = self.create_client_in_db()
		url = reverse('manage-client', args=[client.client_id])

		updated = self.client.patch(
			url,
			data=json.dumps({'name': 'Updated service'}),
			content_type='application/json',
		)
		self.assertEqual(updated.status_code, 200)
		self.assertEqual(updated.json()['client']['name'], 'Updated service')

		deleted = self.client.delete(url)
		self.assertEqual(deleted.status_code, 200)
		client.refresh_from_db()
		self.assertFalse(client.is_active)
