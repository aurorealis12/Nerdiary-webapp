from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

User = get_user_model()
PASSWORD = "Zielony-Smok-4821"


class AuthApiTests(APITestCase):
    def setUp(self):
        cache.clear()  # resets throttle counters between tests
        self.client = APIClient(enforce_csrf_checks=True)

    def post(self, name, data=None):
        """POST with a fresh CSRF token (login rotates it)."""
        token = self.client.get(reverse("auth-csrf")).data["csrfToken"]
        return self.client.post(reverse(name), data or {}, format="json", HTTP_X_CSRFTOKEN=token)

    def registration(self, **changes):
        data = {"username": "alice", "email": "alice@example.com", "password": PASSWORD}
        return {**data, **changes}

    def create_user(self, **changes):
        return User.objects.create_user(**self.registration(**changes))

    def me(self):
        return self.client.get(reverse("auth-me"))

    def test_register_hashes_password_and_logs_in(self):
        response = self.post("auth-register", self.registration(email="Alice@Example.com"))
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)
        user = User.objects.get(username="alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertEqual(self.me().status_code, 200)

    def test_register_cannot_grant_admin_rights(self):
        response = self.post("auth-register", self.registration(is_staff=True, is_superuser=True))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="alice")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_rejects_weak_password(self):
        response = self.post("auth-register", self.registration(password="12345678"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
        self.assertFalse(User.objects.exists())

    def test_register_rejects_duplicates_ignoring_case(self):
        self.create_user()
        response = self.post(
            "auth-register", self.registration(username="ALICE", email="ALICE@example.com")
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_register_and_login_require_csrf_token(self):
        for name in ("auth-register", "auth-login"):
            response = self.client.post(reverse(name), self.registration(), format="json")
            self.assertEqual(response.status_code, 403, name)
        self.assertFalse(User.objects.exists())

    def test_login_and_me(self):
        self.create_user()
        response = self.post("auth-login", {"username": "alice", "password": PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.me().data["username"], "alice")

    def test_failed_logins_look_the_same(self):
        self.create_user()
        wrong = self.post("auth-login", {"username": "alice", "password": "wrong"})
        unknown = self.post("auth-login", {"username": "nobody", "password": "wrong"})
        self.assertEqual(wrong.status_code, 400)
        self.assertEqual(unknown.status_code, 400)
        self.assertEqual(wrong.data, unknown.data)

    def test_inactive_user_cannot_log_in(self):
        user = self.create_user()
        user.is_active = False
        user.save()
        response = self.post("auth-login", {"username": "alice", "password": PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_login_is_throttled(self):
        data = {"username": "alice", "password": "wrong"}
        for _ in range(10):
            self.assertEqual(self.post("auth-login", data).status_code, 400)
        self.assertEqual(self.post("auth-login", data).status_code, 429)

    def test_me_requires_login(self):
        self.assertEqual(self.me().status_code, 403)

    def test_logout_requires_csrf_and_ends_session(self):
        self.create_user()
        self.post("auth-login", {"username": "alice", "password": PASSWORD})
        self.assertEqual(self.client.post(reverse("auth-logout")).status_code, 403)
        self.assertEqual(self.me().status_code, 200)
        self.assertEqual(self.post("auth-logout").status_code, 204)
        self.assertEqual(self.me().status_code, 403)

    def test_home_stays_public(self):
        self.assertEqual(self.client.get(reverse("home-data")).status_code, 200)
