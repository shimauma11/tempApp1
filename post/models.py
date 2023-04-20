from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"], name="like_unique"
            ),
        ]


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)


class Like_for_comment(models.Model):
    user = models.ForeignKey(
        User, related_name="likes_for_comment", on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment, related_name="likes_for_comment", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"], name="like_for_comment_unique"
            ),
        ]
