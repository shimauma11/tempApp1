from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="follower"
    )
