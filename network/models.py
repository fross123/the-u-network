from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return f"{self.content} by {self.user.username} has {self.likes} likes"
