from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)


class FriendShip(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followings",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="friendship_unique"
            ),
        ]
