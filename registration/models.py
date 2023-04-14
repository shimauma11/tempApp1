from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)


class FriendShip(models.Model):
    request_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["request_user", "follower"], name="friendship_unique"
            ),
        ]
