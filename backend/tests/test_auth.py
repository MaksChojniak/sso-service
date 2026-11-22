import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthViewsTests(TestCase):
    def post_json(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json',
        )

    def test_register_creates_user_and_logs_in(self):
        url = reverse('auth-register')
        payload = {
            'email': 'bob@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'Bob',
            'last_name': 'Doe',
            'country': 'PL',
            'phone_number': '+48123456789',
        }
        res = self.post_json(url, payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data['user']['email'], 'bob@example.com')
        self.assertEqual(data['user']['country'], 'PL')

        # Verify session
        me_res = self.client.get(reverse('auth-me'))
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.json()['authenticated'])
        self.assertEqual(me_res.json()['user']['email'], 'bob@example.com')

    def test_register_duplicate_email_fails(self):
        User.objects.create_user(email='existing@example.com', password='password123')
        url = reverse('auth-register')
        payload = {
            'email': 'existing@example.com',
            'password': 'StrongPassword123!',
        }
        res = self.post_json(url, payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn('email', res.json()['errors'])

    def test_login_success_and_logout(self):
        User.objects.create_user(email='charlie@example.com', password='ValidPassword123!')
        login_url = reverse('auth-login')

        # Invalid password
        fail_res = self.post_json(login_url, {'email': 'charlie@example.com', 'password': 'wrong'})
        self.assertEqual(fail_res.status_code, 400)

        # Valid login
        ok_res = self.post_json(login_url, {'email': 'charlie@example.com', 'password': 'ValidPassword123!'})
        self.assertEqual(ok_res.status_code, 200)
        self.assertEqual(ok_res.json()['status'], 'authenticated')

        # Logout
        logout_res = self.client.post(reverse('auth-logout'))
        self.assertEqual(logout_res.status_code, 200)

        me_res = self.client.get(reverse('auth-me'))
        self.assertFalse(me_res.json()['authenticated'])

    def test_admin_login_requires_staff_or_admin_flag(self):
        User.objects.create_user(email='regular@example.com', password='RegularPassword123!')
        User.objects.create_user(
            email='admin@example.com',
            password='AdminPassword123!',
            is_admin_user=True,
        )

        admin_login_url = reverse('admin-auth-login')

        # Regular user fails
        regular_res = self.post_json(admin_login_url, {'email': 'regular@example.com', 'password': 'RegularPassword123!'})
        self.assertEqual(regular_res.status_code, 400)

        # Admin user succeeds
        admin_res = self.post_json(admin_login_url, {'email': 'admin@example.com', 'password': 'AdminPassword123!'})
        self.assertEqual(admin_res.status_code, 200)
        self.assertEqual(admin_res.json()['status'], 'authenticated')

    def test_rate_limiting_on_login(self):
        from django.core.cache import cache
        cache.clear()

        login_url = reverse('auth-login')
        payload = {'email': 'rate@example.com', 'password': 'invalid'}

        # Execute requests up to limit (10 allowed)
        for _ in range(10):
            res = self.post_json(login_url, payload)
            self.assertEqual(res.status_code, 400)

        # 11th request triggers rate limit (429)
        res = self.post_json(login_url, payload)
        self.assertEqual(res.status_code, 429)
        self.assertEqual(res.json()['error'], 'too_many_requests')
        cache.clear()


