from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)


class FriendShip(models.Model):
    request_User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower",
    )

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )