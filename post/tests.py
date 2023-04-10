from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("post:home")
        User.objects.create(
            username="user01", password="testpassword01"
        )
        self.client.login(username="user01", password="testpassword01")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        