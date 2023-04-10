from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, SESSION_KEY
from django.conf import settings

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("registration:signup")
        valid_data = {
            "username": "testuser1",
            "email": "test1@example.com",
            "password1": "testuserpassword1",
            "password2": "testuserpassword1",
        }
        self.client.post(self.url, valid_data)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testuserpassword",
            "password2": "testuserpassword",
        }

        response = self.client.post(self.url, valid_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(
            User.objects.filter(username=valid_data["username"]).exists()
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "testuserpassword",
            "password2": "testuserpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testuserpassword",
            "password2": "testuserpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_duplicated_user(self):
        invalid_data = {
            "username": "testuser1",
            "email": "test1@example.com",
            "password1": "testuserpassword1",
            "password2": "testuserpassword1",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["username"], ["同じユーザー名が既に登録済みです。"])
        self.assertFalse(form.is_valid())

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "testuserpassword",
            "password2": "testuserpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["email"], ["有効なメールアドレスを入力してください。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "ko3ko",
            "password2": "ko3ko",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["password2"], ["このパスワードは短すぎます。最低 8 文字以上必要です。"]
        )
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testuser",
            "password2": "testuser",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["password2"], ["このパスワードは ユーザー名 と似すぎています。"]
        )
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_post_with_only_num_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["password2"],
            [
                "このパスワードは短すぎます。最低 8 文字以上必要です。",
                "このパスワードは一般的すぎます。",
                "このパスワードは数字しか使われていません。",
            ],
        )
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )

    def test_failure_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["password2"], ["確認用パスワードが一致しません。"])
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )


class TestLoginView(TestCase):
    def setUp(self):
        self.url = reverse("registration:login")
        User.objects.create_user(
            username="user01",
            email="user01@example.com",
            password="testpassword01",
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "user01",
            "password": "testpassword01",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

    def test_failure_with_not_exist_user(self):
        not_exist_data = {
            "username": "user02",
            "password": "password02",
        }
        response = self.client.post(self.url, not_exist_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["__all__"],
            ["正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"],
        )

    def test_failure_with_empty_password(self):
        data = {
            "username": "user01",
            "password": "",
        }
        response = self.client.post(self.url, data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["password"], ["このフィールドは必須です。"])


class TestLogoutView(TestCase):
    def setUp(self):
        User.objects.create_user(username="user01", password="password01")
        self.client.login(username="user01", password="password01")
        self.url = reverse("registration:logout")

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("registration:login"),
            status_code=302,
            target_status_code=200,
        )
