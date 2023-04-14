from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("post:home")
        User.objects.create_user(username="user01", password="testpassword01")
        self.client.login(username="user01", password="testpassword01")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["postList"],
            Post.objects.all(),
            ordered=False,
        )


class TestDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user01",
            email="user01@example.com",
            password="testpassword01",
        )
        self.client.login(username="user01", password="testpassword01")
        self.post = Post.objects.create(
            user=self.user, title="testtitle", content="testcontent"
        )
        self.url = reverse("post:detail", kwargs={"pk": self.post.pk})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestCreatePostView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser01", password="testpassword01"
        )
        self.client.login(username="testuser01", password="testpassword01")
        self.url = reverse("post:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {"title": "testtitle", "content": "testcontent"}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("post:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Post.objects.filter(title=data["title"]).exists())

    def test_failure_post_with_empty_content(self):
        data = {"title": "testtitle", "content": ""}
        response = self.client.post(self.url, data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["content"],
            ["このフィールドは必須です。"],
        )
        self.assertFalse(Post.objects.filter(title=data["title"]).exists())

    def test_failure_with_too_long_content(self):
        data = {"title": "testtitle", "content": "a" * 401}
        response = self.client.post(self.url, data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            form.errors["content"],
            ["この値は 400 文字以下でなければなりません( 401 文字になっています)。"],
        )
        self.assertFalse(Post.objects.filter(title=data["title"]).exists())


class TestDeletePost(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="user01@example.com",
            password="testpassword01",
        )
        self.post01 = Post.objects.create(
            user=self.user01, title="testtitle01", content="testcontent01"
        )

    def test_success_post(self):
        self.url = reverse("post:delete", kwargs={"pk": self.post01.pk})
        self.client.login(username="testuser01", password="testpassword01")
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("post:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Post.objects.filter(pk=self.post01.pk).exists())

    def test_failure_with_not_exist_post(self):
        self.url = reverse("post:delete", kwargs={"pk": 1000})
        self.client.login(username="testuser01", password="testpassword01")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 1)

    def test_failure_with_incorrect_user(self):
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="user02@example.com",
            password="testpassword02",
        )
        self.client.login(username="testuser02", password="testpassword02")
        self.url = reverse("post:delete", kwargs={"pk": self.post01.pk})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post01.pk).exists())


class TestProfileView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="test01@example.com",
            password="testpassword01",
        )
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="test02@example.com",
            password="testpassword02",
        )
        self.client.login(username="testuser01", password="testpassword01")
        Post.objects.create(
            user=self.user02,
            title="testtitle",
            content="testcontent",
        )
        self.url = reverse(
            "post:profile",
            kwargs={"pk": self.user02.pk, "username": self.user02.username},
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestFollowView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="test01@example.com",
            password="testpassword01",
        )
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="test02@example.com",
            password="testpassword02",
        )
        Post.objects.create(
            user=self.user01,
            title="testtitle",
            content="testcontent",
        )
        Post.objects.create(
            user=self.user02,
            title="testtitle",
            content="testcontent",
        )
        self.client.login(username="testuser01", password="testpassword01")

    def test_success_post(self):
        self.url = reverse(
            "post:follow",
            kwargs={"username": self.user01.username, "pk": self.user01.pk},
        )
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse(
                "post:profile",
                kwargs={
                    "username": self.user01.username,
                    "pk": self.user01.pk,
                },
            ),
            status_code=302,
            target_status_code=200,
        )
