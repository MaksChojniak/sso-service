import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from models.clients import ClientApplication


User = get_user_model()


class ClientApplicationApiTests(TestCase):
	def setUp(self):
		self.staff_user = User.objects.create_user(
			username='staff',
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

	def post_json(self, url, data):
		return self.client.post(
			url,
			data=json.dumps(data),
			content_type='application/json',
		)

	def test_management_requires_staff(self):
		url = reverse('manage-clients')
		self.assertEqual(self.client.get(url).status_code, 401)
		self.client.force_login(User.objects.create_user(username='regular', password='password'))
		self.assertEqual(self.client.get(url).status_code, 403)

	def test_staff_can_create_and_list_client(self):
		self.client.force_login(self.staff_user)

		created = self.post_json(reverse('manage-clients'), self.payload())

		self.assertEqual(created.status_code, 201)
		client_id = created.json()['client']['client_id']
		self.assertEqual(len(client_id), 36)
		listed = self.client.get(reverse('manage-clients'))
		self.assertEqual(listed.status_code, 200)
		self.assertEqual(listed.json()['count'], 1)

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
		client = ClientApplication.objects.create(**self.payload())
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