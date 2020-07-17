from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, related_name='followers', symmetrical=False)

class Post(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=False, related_name='liked')
    date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        likes = []
        for like in self.likes.all():
            likes.append(like.username)
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.username,
            "likes": self.likes.count(),
            "liked": likes,
            "date": self.date
        }

    def __str__(self):
        return f"{self.content} by {self.user.username} has {self.likes} likes"
