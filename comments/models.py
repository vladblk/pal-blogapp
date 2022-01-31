from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE) # each Comment is related to a single User
    post = models.ForeignKey(Post, on_delete=CASCADE) # each Comment is related to a single Post
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body